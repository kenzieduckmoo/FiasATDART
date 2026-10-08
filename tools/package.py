from pathlib import Path
import re,zipfile
root=Path(__file__).resolve().parents[1]
version=re.search(r'^## Version:\s*(\S+)',(root/'FiammaCollector.toc').read_text(),re.M).group(1)
out=root.parent/f'FiammaCollector-{version}.zip'
excluded={'.git','.github','__pycache__','.pytest_cache'}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        if p.is_file() and not excluded.intersection(p.relative_to(root).parts) and p.name!='.gitignore':
            z.write(p,Path('FiammaCollector')/p.relative_to(root))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert 'FiammaCollector/FiammaCollector.toc' in z.namelist()
print(out)
