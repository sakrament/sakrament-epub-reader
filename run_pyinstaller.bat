
rd /q /s build
rd /q /s dist
rm *.spec

pyinstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --name sakrament_epub_reader ^
  --console ^
  --add-data="data\bin\win32;data\bin\win32" ^
  --add-data="data\db;data\db" ^
  .\sakrament_epub_reader\__main__.py
