```scala
// 1 get fs object
Configuration conf = new Configuration();
conf.set("dfs.replication", "2");
FileSystem fs  = FileSystem.get(new URI("hdfs:hadoop102:9000"), conf, "username");

//2 execute API

// ## 拷贝到hdfs
fs.copyFromLocalFile(new Path("e:/banzhang.txt"), new Path("/xiaohua.txt"));

// ## 拷贝到本地
fs.copyToLocalFile(new Path("/banhua.txt"), new Path("e:/banhua.txt"));

// ## 删除  delete(path, recursive)
fs.delete(new Path("/0529"), true)

// ## 重命名
fs.rename(new Path("/banzhang.txt"), new Path("/yanjing.txt"))


// ## 查看文件 信息 listFiles(path, recursive)
RemoteIterator<LocatedFileStatus> listFiles = fs.listFiles(new Path("/"), true);
while (listFiles.hasnext()){
    LocatedFileStatus fileStatus = listFiles.next();

    //查看文件名称，权限，长度，块信息
    System.out.println(listFiels.getPath().getName());
    System.out.println(listFiels.getPermission());
    System.out.println(listFiels.getLen());

    BlockLocationp[] blockLocations = fileStatus.getBlockLocations();
    for (BlockLocation blockLocation: blocaLocations){
        String[] hosts = blockLocation.getHosts();
        for (String host: hosts){
            System.out.println(host);
        }
    }
    System.out.println("---------------");
}

// ## 判断是文件还是文件夹
FileStatus[] listStatus = fs.listStatus(new Paht("/"));
for (FileStatus fileStatus: listStatus){
    if(fileStatus.isFile()){
        System.out.println("f:" + fileStatus.getPath().getName());
    }
    else{
        System.out.println("d:" + fileStatus.getPath().getName());
    }
}


//3
fs.close();
```