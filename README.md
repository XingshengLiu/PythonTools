# PythonTools
**reNameTool 用于从留置平台下载无规律文件名的整理命名，及生成语音识别所需要用的表格**
  
  *用法*：需要在工具的同目录放一张表格context.xls 表格从第二行开始录入数据，第一列 写入音频文件对应的语音内容，第二列输入下载的原始文件名(注意，文件名需要带.pcm后缀名)，然后运行工具，会生成reName.bat批处理工具，和一个result.xls文件，xls文件即最后语音识别需要使用的文件，点击运行批处理后，所有的文件名会变成xls文件中列出的文件名
  
**meaningUnderstandingTool 用于语义测试pc工具生成的文件和导入的原文件进行对比，生成语义对比的结果**
  
  *用法*：需要生成两个excel文件放在和脚本的统计目录，original.xls 和 result.xls, original 里边添加最原始生成的问法汇总，第一列添加问法，第二列添加期望的意图，result 里边添加PC工具跑出来的有结果的问法汇总，第一列添加问法，第二列添加是被出来的意图，最后会生成resultunderstanding.xls 其中-1是意图有冲突，1是识别正确，null是pc工具识别没有意图的

**randomChooseTool 用于从生成的问法中随机筛选指定条数的数据，生成xls文件，用于测试语义识别率**

  *用法*：把生成xlsx问法文件，放入和工具同目录，运行工具后，会生成xlsx对应数目的xls文件，xls文件即随机筛选的问法

**chooseFilesTool 用于根据表格中的文件筛选pcm文件，或者根据pcm文件重新生成一张表格**

  *用法*：把需要筛选的Excel和pcm文件放到同级目录中，运行工具，选1是根据excel挑选出相应的pcm文件，并且移动至test目录下，test目录需要手动建好，注意表格内容第二列文件名需要带.pcm后缀；选择2，根据pcm文件生成新的excel文件，原始的excel名需要修改为original.xls，第二列文件名同样需要带有.pcm后缀，运行后，会生成chosen.xls，即为重新筛选的excel文件