using System;
using System.Text;
using TestLibrary;

class EncodingGetMaxByteCount
{
    static int Main()
    {
        EncodingGetMaxByteCount test = new EncodingGetMaxByteCount();

        TestFramework.BeginTestCase("Encoding.GetMaxByteCount");

        if (test.RunTests())
        {
            TestFramework.EndTestCase();
            TestFramework.LogInformation("PASS");
            return 100;
        }
        else
        {
            TestFramework.EndTestCase();
            TestFramework.LogInformation("FAIL");
            return 0;
        }

    }

    public bool RunTests()
    {
        bool ret = true;

        // Positive Tests

        ret &= Test1();
        ret &= Test2();
        ret &= Test3();
    
        ret &= Test10();

        ret &= Test11();
        ret &= Test12();
        ret &= Test13();
        ret &= Test14();
        ret &= Test15();

        ret &= Test16();
        ret &= Test17();
        ret &= Test18();

        // Negative Tests

        ret &= Test19();
        ret &= Test20();
   
        ret &= Test25();
        ret &= Test26();
        ret &= Test29();
        ret &= Test30();
        ret &= Test31();
        ret &= Test32();

        return ret;
    }

    // Positive Tests
    public bool Test1() { return PositiveTest(Encoding.UTF8, 0, 3, "00A"); }
    public bool Test2() { return PositiveTest(Encoding.UTF8, 1, 6, "00B"); }
    public bool Test3() { return PositiveTest(Encoding.UTF8, 100, 303, "00C"); }

    public bool Test10() { return PositiveTest(Encoding.Unicode, 0, 2, "00A3"); }
    public bool Test11() { return PositiveTest(Encoding.Unicode, 1, 4, "00B3"); }
    public bool Test12() { return PositiveTest(Encoding.Unicode, 100, 202, "00C3"); }

    public bool Test13() { return PositiveTest(Encoding.BigEndianUnicode, 0, 2, "00A4"); }
    public bool Test14() { return PositiveTest(Encoding.BigEndianUnicode, 1, 4, "00B4"); }
    public bool Test15() { return PositiveTest(Encoding.BigEndianUnicode, 100, 202, "00C4"); }

    public bool Test16() { return PositiveTest(Encoding.UTF8, 0, 3, "00A5"); }
    public bool Test17() { return PositiveTest(Encoding.UTF8, 1, 6, "00B5"); }
    public bool Test18() { return PositiveTest(Encoding.UTF8, 100, 303, "00C5"); }

    //Negative Tests
    public bool Test19() { return NegativeTest(Encoding.UTF8, -1, typeof(ArgumentOutOfRangeException), "00D6"); }
    public bool Test20() { return NegativeTest(Encoding.UTF8, Int32.MaxValue, typeof(ArgumentOutOfRangeException), "00E6"); }

    public bool Test25() { return NegativeTest(Encoding.Unicode, Int32.MaxValue, typeof(ArgumentOutOfRangeException), "00E9"); }
    public bool Test26() { return NegativeTest(Encoding.Unicode, -1, typeof(ArgumentOutOfRangeException), "00D9"); }
    public bool Test29() { return NegativeTest(Encoding.BigEndianUnicode, -1, typeof(ArgumentOutOfRangeException), "00DA"); }
    public bool Test30() { return NegativeTest(Encoding.BigEndianUnicode, Int32.MaxValue, typeof(ArgumentOutOfRangeException), "00EA"); }
    public bool Test31() { return NegativeTest(Encoding.UTF8, Int32.MaxValue, typeof(ArgumentOutOfRangeException), "00EB"); }
    public bool Test32() { return NegativeTest(Encoding.UTF8, -1, typeof(ArgumentOutOfRangeException), "00DB"); }

    public bool PositiveTest(Encoding enc, int input, int expected, string id)
    {
        bool result = true;
        TestFramework.BeginScenario(id + ": Getting max bytes for " + input + " with encoding " + enc.WebName);
        try
        {
            int output = enc.GetMaxByteCount(input);
            if (output != expected)
            {
                result = false;
                TestFramework.LogError("001", "Error in " + id + ", unexpected comparison result. Actual count " + output + ", Expected: " + expected);
            }
        }
        catch (Exception exc)
        {
            result = false;
            TestFramework.LogError("002", "Unexpected exception in " + id + ", excpetion: " + exc.ToString());
        }
        return result;
    }


    public bool NegativeTest(Encoding enc, int input, Type excType, string id)
    {
        bool result = true;
        TestFramework.BeginScenario(id + ": Getting max bytes for " + input + " with encoding " + enc.WebName);
        try
        {
            int output = enc.GetMaxByteCount(input);
            result = false;
            TestFramework.LogError("009", "Error in " + id + ", Expected exception not thrown. Actual count " + output + ", Expected exception type: " + excType.ToString());
        }
        catch (Exception exc)
        {
            if (exc.GetType() != excType)
            {
                result = false;
                TestFramework.LogError("010", "Unexpected exception in " + id + ", excpetion: " + exc.ToString());
            }
        }
        return result;
    }
}
