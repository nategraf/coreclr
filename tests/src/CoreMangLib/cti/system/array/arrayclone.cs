using System;
using System.Globalization;
using System.Collections;
/// <summary>
/// Array.Clone
/// </summary>
public class ArrayClone
{
    const int c_MaxValue = 10;
    const int c_MinValue = 0;
    public static int Main()
    {
        ArrayClone ArrayClone = new ArrayClone();

        TestLibrary.TestFramework.BeginTestCase("ArrayClone");
        if (ArrayClone.RunTests())
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
        retVal = PosTest2() && retVal;
        return retVal;
    }
    // Returns true if the expected result is right
    // Returns false if the expected result is wrong
    public bool PosTest1()
    {
        bool retVal = true;

        TestLibrary.TestFramework.BeginScenario("PosTest1:A shallow copy of an Array copies only the elements of the Array");
        try
        {
            Array myOriginalArray = Array.CreateInstance(typeof(Int32), c_MaxValue);
            for(int i=0;i<c_MaxValue;i++)
            {
                myOriginalArray.SetValue(i, i);
            }
            Array myCloneArray = myOriginalArray.Clone() as Array;
            if (myCloneArray.Equals(myOriginalArray))
             {
                TestLibrary.TestFramework.LogError("001", "A shallow copy of an Array copies only the elements of the Array");
                retVal = false;
             }
             int index = 0;
             for (IEnumerator itr = myOriginalArray.GetEnumerator(); itr.MoveNext(); )
             {
                 object current = itr.Current ;
                 if (!current.Equals(myCloneArray.GetValue(index)))
                 {
                     TestLibrary.TestFramework.LogError("002", "the two object should refer to the elements of the original Array ");
                     retVal = false;
                     break;
                 }
                 index++;
             }
         
        }
        catch (Exception e)
        {
            TestLibrary.TestFramework.LogError("002", "Unexpected exception: " + e);
            retVal = false;
        }

        return retVal;
    }
    // Returns true if the expected result is right
    // Returns false if the expected result is wrong
    public bool PosTest2()
    {
        bool retVal = true;

        TestLibrary.TestFramework.BeginScenario("PosTest2: elements only is a reference and may change the refer to ");
        try
        {
            Array myOriginalArray = Array.CreateInstance(typeof(Int32), c_MaxValue);
            for (int i = 0; i < c_MaxValue; i++)
            {
                myOriginalArray.SetValue(i, i);
            }
            Array myCloneArray = myOriginalArray.Clone() as Array;
            myCloneArray.SetValue(c_MaxValue*10, c_MaxValue - 1);
            object current = myOriginalArray.GetValue(c_MaxValue - 1);
            if (current.Equals(myCloneArray.GetValue(c_MaxValue - 1)))
            {
                TestLibrary.TestFramework.LogError("003", " the clone is changed butthe original one should not be changed ");
                retVal = false;
            }
         }
        catch (Exception e)
        {
            TestLibrary.TestFramework.LogError("004", "Unexpected exception: " + e);
            retVal = false;
        }

        return retVal;
    }
   
}



