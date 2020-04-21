# @File  : askhomewor_testUrlSet.py
# @Author: LiuXingsheng
# @Date  : 2019/12/24
# @Desc  :


AskUrlSet = {
    # 通过古诗名或者句子获取古诗详情和秒懂视屏{古诗结构二}
    'getPoetryDetailAndSecondKnow': '/app/search/poetry/getPoetryDetailAndSecondKnow',
    # 根据[古诗名或诗句]获取[诗歌诗句信息]和秒懂视屏
    'getPoetryDetailAndSecondKnowByFuzzyPoetryNameOrSentence': '/app/search/poetry/getPoetryDetailAndSecondKnowByFuzzyPoetryNameOrSentence',
    # 通过古诗ID获取古诗详情和秒懂视屏{古诗结构一}
    'getPoetryDetailAndSecondKnowById': '/app/search/poetry/getPoetryDetailAndSecondKnowById',
    # 根据[诗歌名（不包含符号的纯中文名）或词牌名]获取[诗歌详情]
    'getPoetryDetailAndSecondKnowBySummaryNameOrEpigraph': '/app/search/poetry/getPoetryDetailAndSecondKnowBySummaryNameOrEpigraph',
    # 获取单元好词好句详细数据
    'getArticleCatalogRecommend': '/app/syncArticle/getArticleCatalogRecommend',
    # 搜索同步作文数据
    'searchSyncArticle': '/app/articleOnline/searchSyncArticle',
    # 获取课外作文体裁好词好句详情
    'getArticleExtraStyleRecommendDetail': '/app/extraArticle/getArticleExtraStyleRecommendDetail',
    # 获取同步作文章节下所有作文数据(用于看图写话)
    'getArticleCatalogAllData': '/app/syncArticle/getArticleCatalogAllData',
    # 搜索看图写话数据
    'searchPictrueWriting': '/app/articleOnline/searchPictrueWriting',
    # 获取声母韵母整体认读拼音信息分类〉 〈声母（类型）、韵母（类型）、整体认读、26个字母〉 新增 传入参数letterType值：声母/韵母/整体认读/26个字母
    'getInitialVowelTypeAndSyllableDetailInfos': '/app/search/phonetic/getInitialVowelTypeAndSyllableDetailInfos',
    #  字母H5在线化动画（新增接口）
    'getInitialVowelWholeAnimationByLetter': '/app/search/phonetic/getInitialVowelWholeAnimationByLetter',
    # 根据类型获取对应分词信息  参数type:getFullOrEnglishSegmentersByStr / getEglishPhraseSegmenters (单词纠错优化，参考参数：you’e --> you’re，fayuer-->Father)
    'getSegmentersByType': '/app/segmenter/getSegmentersByType',
    # 根据作文题目获取乐乐作文的请求地址
    'getLeLeCompositionBySameKey': '/app/search/other/getLeLeCompositionBySameKey',
    # 获取同步作文和笔神作文，无结果返回时，返回lele作文
    'getSnyAndBishenAndLeleCompositions': '/app/search/other/getSnyAndBishenAndLeleCompositions',
    # 获取乐乐作文的请求地
    'getLeLeCompositions': '/app/search/other/getLeLeCompositions',
    # 热门问法（新增版本控制，验证接口和功能是否正常）
    'getHotAskMethod': '/app/search/mainPage/getHotAskMethod',
    # 根据机器序列号获取ASR分支
    'getASRInfoByMachineId': '/app/search/other/getASRInfoByMachineId',
    # gradeName=三年级&editionType=人教版&hanziStr=郝&phoneticStr=ho（新增返回结果字段makeCharacter ，writingRule）
    'queryCommonModuleByHanziStrAndphoneticStr1': '/app/search/es/queryCommonModuleByHanziStrAndphoneticStr1',
    # 根据序列号获取活跃用户语料是否上报（2020-2-28大数据活跃用户例如：700S25000948R 700S25000A1AR 700S25000ADF8，自定义活跃用户：700S5940011EX）
    'getUserActiveCorpuss': '/app/search/other/getUserActiveCorpuss',
    #  根据技能名称获取技能信息（接口修改，适配S6机型，保证修改前后S5等机型数据不变）
    'getListBySkillName': '/app/topOperate/getListBySkillName',
    # 〈根据一级技能分类id获取二级分类信息列表〉（接口修改，适配S6机型，保证修改前后S5等机型数据不变）
    'getSkillClassChildListByClassId': '/app/topOperate/getSkillClassChildListByClassId',
    # 〈获取智慧小布首页运营和技能信息 新增返回字段：pic_type
    'getTopOperates': '/app/topOperate/getTopOperates',
    # 智慧小布和规H5返回（新增接口）
    'getLegalComplianceH5': '/app/topOperate/getLegalComplianceH5',
    # 获取机型对应的主题皮肤（新增三个返回字段：horizontalScreenMinImg,verticalScreenMinImg,horizontalThumbnailImg）
    'getThemeSkin': '/app/search/other/getThemeSkin',
    # 获取笔神课外体裁作文信息（新增接口）
    'getArticleExtraMoreStyles': '/app/search/other/getArticleExtraMoreStyles',
    # 获取笔神作文（新增接口）
    'getBishenCompositions': '/app/search/other/getBishenCompositions',
    # 上报机器信息,每个序列号只上报一次,多次上报只记录一次
    'uploadActivationInfo':'/app/machinerecord/uploadActivationInfo'
}

VoiceUrlSet = {'uploadPointQuestionVoiceBaseData': '/api/voiceMaterial/uploadPointQuestionVoiceBaseData',
               'uploadVoiceBaseData': '/api/voiceMaterial/uploadVoiceBaseData',
               'uploadVoiceBaseDataFinger': '/api/voiceMaterial/uploadVoiceBaseDataFinger',
               }
