import java.lang.RuntimeException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class PersonRecord {
    public int Id;
    public String FirstName;
    public String LastName;
    public String PhoneNumber;
    public int Age;
    public int Salary;

    public PersonRecord(int id,String fname,String lname,String pnumber,int age,int salary)
    {
        Id =id;
        FirstName = fname;
        LastName = lname;
        PhoneNumber = pnumber;
        Age = age;
        Salary = salary;
    }
    public static PersonRecord Parse(String str)
    {         
        String [] words = str.split("\\s+");
        if(words.length < 6)
        {
            throw new RuntimeException("Invalid string : "+str);
        }
        return new PersonRecord(
            Integer.parseInt(words[0]),
            words[1],
            words[2],
            words[3],
            Integer.parseInt(words[4]),
            Integer.parseInt(words[5])
        );
    }
    private static final Pattern PersonRecPattern = 
        Pattern.compile("\\s*(\\d+)\\s+(\\w+)\\s+(\\w+)\\s+(\\S+)\\s+(\\d+)\\s+(\\d+)");
    public static PersonRecord ParseRegex(String record)
    {
        Matcher m = PersonRecPattern.matcher(record);
        if(!m.find())
            throw new RuntimeException("Error while parsing " + record);
        return new PersonRecord(Integer.parseInt(m.group(1)),
                                 m.group(2),
                                 m.group(3),
                                 m.group(4),
                                Integer.parseInt(m.group(5)),
                                Integer.parseInt(m.group(6)));                                            
    }
}
