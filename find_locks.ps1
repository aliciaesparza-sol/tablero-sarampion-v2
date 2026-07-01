$code = @"
using System;
using System.Runtime.InteropServices;
using System.Collections.Generic;
public class FileUtil {
    [DllImport("rstrtmgr.dll", CharSet = CharSet.Unicode)]
    public static extern int RmStartSession(out uint pSessionHandle, int dwSessionFlags, string strSessionKey);
    [DllImport("rstrtmgr.dll", CharSet = CharSet.Unicode)]
    public static extern int RmRegisterResources(uint pSessionHandle, uint nFiles, string[] rgsFilenames, uint nApplications, IntPtr rgApplications, uint nServices, IntPtr rgServices);
    [DllImport("rstrtmgr.dll")]
    public static extern int RmGetList(uint pSessionHandle, out uint pnProcInfoNeeded, ref uint pnProcInfo, [In, Out] RM_PROCESS_INFO[] rgAffectedApps, ref uint lpdwRebootReasons);
    [DllImport("rstrtmgr.dll")]
    public static extern int RmEndSession(uint pSessionHandle);
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct RM_PROCESS_INFO {
        public int ProcessId;
        public System.Runtime.InteropServices.ComTypes.FILETIME ProcessStartTime;
        public int AppType;
        public int AppStatus;
        public int TSSessionId;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)] public string AppName;
    }
    public static List<int> GetLockingProcesses(string path) {
        uint handle;
        RmStartSession(out handle, 0, Guid.NewGuid().ToString());
        string[] files = new string[] { path };
        RmRegisterResources(handle, 1, files, 0, IntPtr.Zero, 0, IntPtr.Zero);
        uint needed = 0, count = 0;
        uint reasons = 0;
        RmGetList(handle, out needed, ref count, null, ref reasons);
        if (needed == 0) { RmEndSession(handle); return new List<int>(); }
        RM_PROCESS_INFO[] processes = new RM_PROCESS_INFO[needed];
        RmGetList(handle, out needed, ref count, processes, ref reasons);
        RmEndSession(handle);
        List<int> pids = new List<int>();
        for (int i = 0; i < count; i++) pids.Add(processes[i].ProcessId);
        return pids;
    }
}
"@
Add-Type -TypeDefinition $code -ErrorAction SilentlyContinue
$path = 'C:\Users\aicil\AppData\Local\Packages\Claude_pzs8sxrjxfjjc'
$pids = [FileUtil]::GetLockingProcesses($path)
if ($pids.Count -gt 0) {
    Get-Process -Id $pids -ErrorAction SilentlyContinue | Select-Object Id, Name, Path
} else {
    Write-Host "No processes found locking $path"
}
