$steam = Get-Process steam -ErrorAction SilentlyContinue
if ($steam) {
  $steam.CloseMainWindow()
  Sleep 5
  if (!$steam.HasExited) {
    $steam | Stop-Process -Force
  }
}
 
Remove-Variable steam
start-process .\Ice.exe
$ice = Get-process ice
while(!$ice.HasExited){

}
 Remove-Variable ice

 start-process "steam:"
