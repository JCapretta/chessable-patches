#!/usr/bin/env python3
"""Audit a Morphe-produced APK without retaining app code in the repository."""
import hashlib
from pathlib import Path
import re
import struct
import sys
import zipfile


def verify(original_path, patched_path):
    source = (Path(__file__).resolve().parents[1] /
              'patches/src/main/kotlin/com/jcapretta/chessable/folders/FolderReviewEdits.kt').read_text()
    expected_hash = re.search(r'ORIGINAL_SHA256 = "([0-9a-f]+)"', source).group(1)
    edits = re.findall(r'edit\("([^"]+)", (0x[0-9a-f]+), "([0-9a-f]+)", "([0-9a-f]+)"\)', source)
    assert edits, 'No declared edits found'
    with zipfile.ZipFile(original_path) as original_zip, zipfile.ZipFile(patched_path) as patched_zip:
        original = original_zip.read('assets/index.android.bundle')
        patched = patched_zip.read('assets/index.android.bundle')
    assert hashlib.sha256(original).hexdigest() == expected_hash, 'Unsupported original bundle'
    assert len(original) == len(patched), 'Bundle length changed'
    assert struct.unpack_from('<I', patched, 32)[0] == len(patched), 'Invalid header file length'
    assert hashlib.sha1(patched[:-20]).digest() == patched[-20:], 'Invalid Hermes footer'
    expected = bytearray(original)
    for name, offset, before, after in edits:
        offset = int(offset, 16)
        before, after = bytes.fromhex(before), bytes.fromhex(after)
        assert original[offset:offset + len(before)] == before, f'{name}: wrong original instructions'
        assert patched[offset:offset + len(after)] == after, f'{name}: patch was not applied'
        expected[offset:offset + len(before)] = after
        print(f'PASS {name}')
    expected[-20:] = hashlib.sha1(expected[:-20]).digest()
    assert patched == expected, 'Unexpected changes outside the declared edits'
    print(f'PASS bounded changes and checksum; bundle SHA-256: {hashlib.sha256(patched).hexdigest()}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: verify-patched-apk.py ORIGINAL.apk PATCHED.apk')
    try:
        verify(*sys.argv[1:])
    except (AssertionError, OSError, KeyError, zipfile.BadZipFile) as error:
        sys.exit(f'FAIL: {error}')
