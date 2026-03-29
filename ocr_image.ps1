
[Reflection.Assembly]::LoadWithPartialName("System.Drawing") | Out-Null
[Reflection.Assembly]::LoadWithPartialName("System.IO") | Out-Null
Add-Type -AssemblyName "Windows.Media.Ocr, ContentType=WindowsRuntime"
Add-Type -AssemblyName "Windows.Graphics.Imaging, ContentType=WindowsRuntime"
Add-Type -AssemblyName "Windows.Storage.Streams, ContentType=WindowsRuntime"

function Get-OcrText {
    param([string]$ImagePath)
    
    $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync($ImagePath).GetResults()
    $stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetResults()
    
    $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetResults()
    $bitmap = $decoder.GetSoftwareBitmapAsync().GetResults()
    
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    if ($engine -eq $null) {
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new("es-ES"))
    }
    
    $result = $engine.RecognizeAsync($bitmap).GetResults()
    return $result.Text
}

$imagePath = $args[0]
if ($imagePath -and (Test-Path $imagePath)) {
    $fullPath = Resolve-Path $imagePath
    Get-OcrText -ImagePath $fullPath
}
