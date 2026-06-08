$BadList = @("m365copilot", "OneDrive", "OneDrive.Sync.Service", "MicrosoftEdgeUpdate", "Cortana", "TestNullprocess2");

Write-Host("Being running DisableUnwantedProcesses Program!") -ForegroundColor Green;

foreach ($B in $BadList)
{
    $Cache = Get-Process $B -ErrorAction SilentlyContinue;

    if (-not ($Cache))
    {
        Write-Host("Process $B does not exist or is not running.") -ForegroundColor Yellow;
        continue;
    }

    Write-Host("Process $B Has been found and will be disabled!") -ForegroundColor Green;

    try
    {
        Stop-Process -name $B -ErrorAction SilentlyContinue;
    }
    catch
    {
        Write-Host("Failed to stop process $B, continuing") -ForegroundColor Red;
        continue;
    }
    finally
    {
        Write-Host("Succeeding in stopping process $B!") -ForegroundColor Green;
    }
    
}

Write-Host("Finished running DisableUnwantedProcesses Program!") -ForegroundColor Green;