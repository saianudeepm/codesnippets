This below code explains the structure of how a map reduce job can be coded.

For actual example, refer to this [repo](https://github.com/mahmoudparsian/data-algorithms-book/tree/master/src/main/java/org/dataalgorithms/chap02/mapreduce)

##Driver to run the mapreduce job
```
public class Driver implements Tool {
	@Override
	public int run(String args[]){
		//create a configuration
		Configuration conf = getConf();
		//create a new job using the config obj
		Job job = Job.getInstance(conf);
		job.setJarByClass(	Driver.class);
		job.setJobName("yeahhhh");
		
		//specify the inputFormat and outputformat 
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		/*
		Alternative way to set custom inputformat and custom outputformat
		For eg when we have a lot of small files -> MapReduce job for packaging small files into sequence files
		//class WholeFileInputFormat extends FileInputFormat<NullWritable, BytesWritable> //custom input format
		//class WholeFileRecordReader extends RecordReader<NullWritable, BytesWritable> //custom record reader
		job.setInputFormatClass(WholeFileInputFormat.class); 
		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(BytesWritable.class);
		*/
		
		//set key class and output class 
		job.setOutputKeyClass(DateTemperaturePair.class);
		job.setOutputValueClass(Text.class);
	
		//set map and reduce classes to be used for the job
		job.setMapperClass(SecondarySortMapper.class);
		job.setReducerClass(SecondarySortReducer.class);	
		
		//Alternatively also configure the partitioner
		job.setPartitionerClass(DateTemperaturePartitioner.class);
		
		// And also specify how the keys should be grouped on the reducer by specifying custom GroupingComparator
		job.setGroupingComparatorClass(DateTemperatureGroupingComparator.class);
		
		// Specify how the keys should be sorted on the reducer by specifying a custom SortComparator
		job.setSortComparatorClass(CompositeKeyComparator.class);
		//now wait for completion
		boolean status = job.setWaitForCompletion(true);
	}

	public int submitJob(){
		int returnStatus = ToolRunner.run(new Driver(), args);
	}
}
```

##Mapper class 
```
public class MyMapper extends Mapper<KEYIN, VALUEIN, KEYOUT, VALUEOUT>{
	
	//we process and write to context the key,value pair that needs to be sent to the Reducer
	@Overwrite
	protected void map(KEYIN key, VALUEIN value, 
                     Context context) throws IOException, InterruptedException {
    context.write((KEYOUT) key, (VALUEOUT) value);
  }

//Mapper class has a run method which gets essentially calls the map method for every key value with the context . Finally cleans up
//Default implementation (Mapper Task)
public void run(Context context) throws IOException, InterruptedException {
    setup(context);
    try {
      while (context.nextKeyValue()) {
        map(context.getCurrentKey(), context.getCurrentValue(), context);
      }
    } finally {
      cleanup(context);
    }
  }



}
```

##Reducer class
```
public class MyReducer extends Reducer<KEYIN,VALUEIN,KEYOUT,VALUEOUT>{
	

	@Override
	protected void reduce(KEYIN key, Iterable<VALUEIN> values, Context context
                        ) throws IOException, InterruptedException {
    for(VALUEIN value: values) {
      context.write((KEYOUT) key, (VALUEOUT) value);
    }
  }

}
```

##Custom Partitioner class
```
public class MyPartitioner extends Partitioner<KEY,VALUE>{
	
 //implement this method and return the bucket or partition number
 public int getPartition(KEY key, VALUE value, int numPartitions){


 }

}
```

##Custom GroupingComparator class (Similar approach for a SortComparator)
```
//To specify a custom Comparator for grouping the values for reducer use a class that implements the RawComparator Interface
public interface RawComparator<T> extends Comparator<T> {
	
}

one example will be WritableComparator and implement the compare() method

public class MyGroupingComparator 
   extends WritableComparator {
   
   //Here wc1 and wc2 are the keys sent from Mapper. type cast them to the respective keys and compareTo and return an int
   @Overwrite
   public int compare(WritableComparable wc1, WritableComparable wc2) {
        return pair.getYearMonth().compareTo(pair2.getYearMonth());
    }
   }
```

