
rd /q /s build
rd /q /s dist
rm *.spec

pyinstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --name sakrament_epub_reader ^
  --console ^
  --add-data="sakrament_epub_reader\data;data" ^
  .\sakrament_epub_reader\__main__.py
