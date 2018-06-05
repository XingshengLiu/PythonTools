# PythonTools
**reNameTool 用于从留置平台下载无规律文件名的整理命名，及生成语音识别所需要用的表格**
  用法：
  
**meaningUnderstandingTool 用于语义测试pc工具生成的文件和导入的原文件进行对比，生成语义对比的结果**
  *用法*：需要生成两个excel文件放在和脚本的统计目录，original.xls 和 result.xls, original 里边添加最原始生成的问法汇总，第一列添加问法，第二列添加期望的意图，result 里边添加PC工具跑出来的有结果的问法汇总，第一列添加问法，第二列添加是被出来的意图，最后会生成resultunderstanding.xls 其中-1是意图有冲突，1是识别正确，null是pc工具识别没有意图的
