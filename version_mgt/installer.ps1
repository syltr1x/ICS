mkdir ICS
curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/main.pyw -o ICS/main.pyw
curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/logic.py -o ICS/logic.py

mkdir ICS/frames
$frames_list=curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/frames_list
$frames_list=$frames_list -split "_"
foreach($frame in $frames_list) {
    curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/frames/$frame -o ICS/frames/$frame
}

mkdir ICS/img
$img_list=curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/img_list
$img_list=$img_list -split "_"
foreach($img in $img_list) {
    curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/img/$img -o ICS/img/$img
}

curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/requirements.txt -o ICS/requirements.txt
py -m pip install -r ICS/requirements.txt

$pydirs=python -c "import sys; print(sys.path)"
$pydirs = $pydirs -replace "[\[\]'']", ""
$pydirs = $pydirs -split ", "

foreach($pdir in $pydirs) {
    if ($pdir -match "site-packages") {
        $pdir = $pdir
        break
    }
}
curl.exe https://raw.githubusercontent.com/syltr1x/mythings/main/ctk_mod/red.json -o C:\Users\r4y\AppData\Local\Programs\Python\Python311\Lib\site-packages\customtkinter\assets\themes\red.json
