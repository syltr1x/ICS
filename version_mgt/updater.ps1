$version_data=curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/version_mgt/vkey
$partes = $version_data -split "_"

$secuencia = $partes[1]

$valores = @()

foreach ($digito in $secuencia.ToCharArray()) {
    if ($digito -eq "1") {
        $valores += $true
    } elseif ($digito -eq "0") {
        $valores += $false
    } else {
        Write-Host "Dígito no reconocido: $digito"
    }
}
if ($valores[0]) {
    rm ICS/main.pyw
    curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/main.pyw -o ICS/main.pyw
} if ($valores[1]) {
    rm ICS/logic.py
    curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/logic.py -o ICS/logic.py
} if ($valores[2]) {
    rm -r ICS/frames
    mkdir ICS/frames
    $frames_list=curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/frames_list
    $frames_list=$frames_list -split "_"
    foreach($frame in $frames_list) {
        curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/frames/$frame -o ICS/frames/$frame
    }
} if ($valores[3]) {
    rm -r ICS/img
    $img_list=curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/img_list
    $img_list=$img_list -split "_"
    foreach($img in $img_list) {
        curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/img/$img -o ICS/img/$img
    }
} if ($valores[4]) {
    rm ICS/requirements.txt
    curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/requirements.txt -o ICS/requirements.txt
}

curl.exe https://raw.githubusercontent.com/syltr1x/ICS/main/vehicles.json -o 'ICS/data/vehicles.json'