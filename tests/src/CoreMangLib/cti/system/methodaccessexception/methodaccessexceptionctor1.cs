using System;
using System.Collections.Generic;
/// <summary>
///Ctor
/// </summary>
public class MethodAccessExceptionCtor1
{
    public static int Main()
    {
        MethodAccessExceptionCtor1 MethodAccessExceptionCtor1 = new MethodAccessExceptionCtor1();

        TestLibrary.TestFramework.BeginTestCase("MethodAccessExceptionCtor1");
        if (MethodAccessExceptionCtor1.RunTests())
        {
            TestLibrary.TestFramework.EndTestCase();
            TestLibrary.TestFramework.LogInformation("PASS");
            return 100;
        }
        else
        {
            TestLibrary.TestFramework.EndTestCase();
            TestLibrary.TestFramework.LogInformation("FAIL");
            return 0;
        }
    }
    public bool RunTests()
    {
        bool retVal = true;
        TestLibrary.TestFramework.LogInformation("[Positive]");
        retVal = PosTest1() && retVal;
        return retVal;
    }
    // Returns true if the expected result is right
    // Returns false if the expected result is wrong
    public bool PosTest1()
    {
        bool retVal = true;
        TestLibrary.TestFramework.BeginScenario("PosTest1: Create a new instance of MethodAccessException.");
        try
        {
            MethodAccessException myException = new MethodAccessException();
            if (myException == null)
            {
                TestLibrary.TestFramework.LogError("001.1", "MethodAccessException instance can not create correctly.");
                retVal = false;
            }
        }
        catch (Exception e)
        {
            TestLibrary.TestFramework.LogError("001.0", "Unexpected exception: " + e);
            retVal = false;
        }
        return retVal;
    }
}
