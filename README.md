# PythonTools
**reNameTool 用于从留置平台下载无规律文件名的整理命名，及生成语音识别所需要用的表格**
  
  *用法*：使用任意命名xlsx文件，文件名可使用中文，和pcm还有excel还有工具放在同级目录，运行工具即可
  
**meaningUnderstandingTool 用于语义测试pc工具生成的文件和导入的原文件进行对比，生成语义对比的结果**
  
  *用法*：需要生成两个excel文件放在和脚本的统计目录，original.xls 和 result.xls, original 里边添加最原始生成的问法汇总，第一列添加问法，第二列添加期望的意图，result 里边添加PC工具跑出来的有结果的问法汇总，第一列添加问法，第二列添加是被出来的意图，最后会生成resultunderstanding.xls 其中-1是意图有冲突，1是识别正确，null是pc工具识别没有意图的

**randomChooseTool 用于从生成的问法中随机筛选指定条数的数据，生成xls文件，用于测试语义识别率**

  *用法*：把生成xlsx问法文件，放入和工具同目录，运行工具后，会生成xlsx对应数目的xls文件，xls文件即随机筛选的问法

**chooseFilesTool 用于根据表格中的文件筛选pcm文件，或者根据pcm文件重新生成一张表格**

  *用法*：把需要筛选的Excel和pcm文件放到同级目录中，运行工具，选1是根据excel挑选出相应的pcm文件，并且移动至test目录下，test目录需要手动建好，注意表格内容第二列文件名需要带.pcm后缀；选择2，根据pcm文件生成新的excel文件，原始的excel名需要修改为original.xls，第二列文件名同样需要带有.pcm后缀，运行后，会生成chosen.xls，即为重新筛选的excel文件

**changeSkillIdTool 用于把生成问法中的中文技能统一替换为数字技能Id**

  *用法*：把需要重新填写技能Id的excel文件放到和工具的同级目录下，excel文件格式三列，data，技能，意图名，运行工具，选择对应的技能数字即可

**tideyDataTool 小工具**

  *用法*：主要参考json的转换方式