# What Windows says of notifications, and its Do Not Disturb as the Settings app switches it (on/off; read: only says).
param([string]$to = 'read')
$ErrorActionPreference = 'Stop'
Add-Type @'
using System.Runtime.InteropServices;
public static class Told { [DllImport("shell32.dll")] public static extern int SHQueryUserNotificationState(out int state); }
'@
if ($to -ne 'read') {
  Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
  Start-Process 'ms-settings:notifications'
  $A = [Windows.Automation.AutomationElement]
  $switch = $null
  foreach ($i in 1..40) {
    Start-Sleep -Milliseconds 500
    $is = New-Object Windows.Automation.PropertyCondition($A::ControlTypeProperty, [Windows.Automation.ControlType]::Button)
    $all = $A::RootElement.FindAll('Descendants', $is)
    $switch = $all | Where-Object { $_.Current.AutomationId -match 'DoNotDisturb|QuietHours|QuietMoments' -or $_.Current.Name -eq 'Do not disturb' } | Select-Object -First 1
    if ($switch) { break }
  }
  if (-not $switch) { 'NOSWITCH ' + (($all | ForEach-Object { $_.Current.Name + '/' + $_.Current.AutomationId }) -join '; '); exit 1 }
  $toggle = $switch.GetCurrentPattern([Windows.Automation.TogglePattern]::Pattern)
  if (($toggle.Current.ToggleState -eq 'On') -ne ($to -eq 'on')) { $toggle.Toggle() }
  Start-Sleep 3
  Get-Process SystemSettings -ErrorAction SilentlyContinue | Stop-Process -Force
  Start-Sleep 1
}
$state = 0
[void][Told]::SHQueryUserNotificationState([ref]$state)
$null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
$mode = [Windows.UI.Notifications.ToastNotificationManager]::GetDefault().NotificationMode
"$state $(if ($null -eq $mode) { 'none' } else { [int]$mode })"
