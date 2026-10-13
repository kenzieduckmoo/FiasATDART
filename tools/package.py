from pathlib import Path
import re,zipfile
root=Path(__file__).resolve().parents[1]
version=re.search(r'^## Version:\s*(\S+)',(root/'FiammaCollector.toc').read_text(),re.M).group(1)
out=root.parent/f'FiammaCollector-{version}.zip'
toc=root/'FiammaCollector.toc'
runtime=[line.strip().replace('\\','/') for line in toc.read_text().splitlines() if line.strip() and not line.lstrip().startswith('#')]
files={toc,root/'LICENSE',root/'README.md',root/'CHANGELOG.md'}
for name in runtime:
    path=(root/name).resolve()
    assert path.is_relative_to(root) and path.is_file(),f'Missing or invalid runtime file: {name}'
    files.add(path)
# Fiamma Collector currently uses Blizzard assets. Include local media if added.
if (root/'Media').is_dir():
    files.update(p for p in (root/'Media').rglob('*') if p.is_file())
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):
        z.write(p,Path('FiammaCollector')/p.relative_to(root))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert 'FiammaCollector/FiammaCollector.toc' in z.namelist()
    for name in runtime:
        assert z.read('FiammaCollector/'+name)==(root/name).read_bytes()
    assert all(name.startswith('FiammaCollector/') for name in z.namelist())
    assert not any(part in {'.git','.github','tests','tools','__pycache__'} for name in z.namelist() for part in name.split('/'))
print(out)
