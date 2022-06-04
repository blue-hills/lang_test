import java.util.TreeMap;
import java.util.Map;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;
import java.lang.RuntimeException;
import java.util.function.Function;

//Use picocli for parsing Command Line Arguments
import picocli.CommandLine.Model.CommandSpec;
import picocli.CommandLine.Model.OptionSpec;
import picocli.CommandLine.ParseResult;
import picocli.CommandLine;

public class LoadPersonRecordFile
{
    private static int RepeatCount  = 100;
    private static String InputFile;
    private static String Algorithm;

    public static Map<Integer,PersonRecord> Load(Function<String,PersonRecord> parseFunc)
    {
        final Map<Integer,PersonRecord> m = new TreeMap<Integer,PersonRecord>();
        try (Stream<String> stream = Files.lines(Paths.get(InputFile))) {
            stream.forEach((String l)->{
                PersonRecord p = parseFunc.apply(l);
                m.put(p.Id,p);
            });
        }
        catch(Exception e)
        {
            System.out.println(e);            
        }
        return m;
    }

    static int ParseArgs(ParseResult pr)
    {
          // handle requests for help or version information
          Integer helpExitCode = CommandLine.executeHelpRequest(pr);
          if (helpExitCode != null) { return helpExitCode; }
          RepeatCount = pr.matchedOptionValue('r', 1);
          InputFile = pr.matchedOptionValue('i',"xx");
          Algorithm = pr.matchedOptionValue('a',"xx");
          return 1;
    }

    private static void ReadArguments(String [] args)
    {
        CommandSpec spec = CommandSpec.create();
        spec.mixinStandardHelpOptions(true);
        spec.addOption(OptionSpec.builder("-r", "--repeat") 
        .paramLabel("REPEAT")
        .type(int.class)
        .description("number of times to execute").build());
        
        spec.addOption(OptionSpec.builder("-i","--input")
        .paramLabel("INPUT")
        .type(String.class)
        .required(true)
        .description("Input File").build());
        
        spec.addOption(OptionSpec.builder("-a","--algo")
        .paramLabel("ALGO")
        .type(String.class)
        .required(true)
        .description("Algorithm to parse: use split or regex").build());

        CommandLine commandLine = new CommandLine(spec);
        commandLine.setExecutionStrategy(LoadPersonRecordFile::ParseArgs);
        commandLine.execute(args);
    }

    public static void RunTests() throws RuntimeException
    {
       Function<String,PersonRecord> parseFunc = (Algorithm =="regex")
           ? PersonRecord::ParseRegex 
           : PersonRecord::Parse;
        
       for(int i=0;i<RepeatCount;++i)
       {
           Map<Integer,PersonRecord> dict = Load(parseFunc);
           if(!dict.containsKey(dict.size()-1))
           {
               throw new RuntimeException("Could not find Person Record for "+ (dict.size()-1) );
           }               
       }
       System.out.println("Executed "+RepeatCount + " times.");   
       System.out.println((Algorithm == "regex" ? "java.util.regex" :"String::split")+" used for parsing.");
    }
    
    public static void main(String []args)
    {
        try 
        {
           ReadArguments(args);           
           RunTests();
        } catch (Exception e) 
        {
            System.out.println(e);
        } 
    }
}
