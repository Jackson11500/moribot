import numpy as np

chatlist2 = {
    "摸": [
        "舒服w，蹭蹭~",
        "好舒服，蹭蹭~",
        "再摸咱就长不高啦～",
        "变态！！不许乱摸",
        "好吧~_~，就一下下哦……唔~好了……都两下了……(害羞)",
    ],
    "摸摸": [
        "舒服w，蹭蹭~",
        "好舒服，蹭蹭~",
        "再摸咱就长不高啦～",
        "变态！！不许乱摸",
        "好吧~_~，就一下下哦……唔~好了……都两下了……(害羞)",
    ],
    "上你": [
        "（把你按在地上）这么弱还想欺负咱，真是不自量力呢",
        "你再这样我就不理你了（＞д＜）"
    ],
    "傻": [
        "超级讨厌你说咱傻的说",
        "你为什么会这么觉得呢(＞﹏＜)",
        "谁是傻子呀？（歪头",
        "呜嘿嘿(￣▽￣)~*",
        "诶嘿嘿嘿~",
        "就多读书",
        "讨厌啦，你最讨厌了(///////)",
        "对呀，我傻得只喜欢你一个人",
        "咱才不傻呢!o(>﹏<)o",
        "咱最讨厌嘴臭的人了",
        "不可以骂别人哟，骂人的孩子咱最讨厌了！",
        "咱遇见喜欢的人就变傻了Q_Q",
        "咱...一定一定会努力变得更聪明的！你就等着那一天的到来吧！"
    ],
    "裸": [
        "下流！",
        "你在想什么呢，敲头！",
        "你这是赤裸裸的性骚扰呢ヽ(`Д´)ノ",
        "你的身体某些地方看起来不太对劲，咱帮你修剪一下吧。（拿出剪刀）",
        "咱认为你的脑袋可能零件松动了，需要打开检修一下。（拿出锤子）"
    ],
    "贴": [
        "贴什么贴.....只......只能......一下哦！",
        "贴...贴贴（靠近）",
        "蹭蹭…你以为咱会这么说吗！baka死宅快到一边去啦！",
        "你把脸凑这么近，咱会害羞的啦Σ>―(〃°ω°〃)♡→",
        "退远",
        "不可以贴"
    ],
    "贴贴": [
        "贴什么贴.....只......只能......一下哦！",
        "贴...贴贴（靠近）",
        "蹭蹭…你以为咱会这么说吗！baka死宅快到一边去啦！",
        "你把脸凑这么近，咱会害羞的啦Σ>―(〃°ω°〃)♡→",
        "退远",
        "不可以贴"
    ],
    "老婆": [
        "见谁都是一口一个老婆的人，要不要把你也变成女孩子呢？(*-`ω´-)✄",
        "神经病，凡是美少女都是你老婆吗？",
        "嘛嘛~本喵才不是你的老婆呢"
        "欸...要把咱做成饼吗？咱只有一个，做成饼吃掉就没有了...",
        "已经可以了，现在很多死宅也都没你这么恶心了",
        "不可以"
    ],
    "抱": [
        "诶嘿~（钻进你怀中）",
        "o(*////▽////*)q",
        "只能一会哦（张开双手）",
        "你就像个孩子一样呢...摸摸头(>^ω^<)抱一下~你会舒服些吗？",
        "嘛，真是拿你没办法呢，就一会儿哦",
        "抱住不忍心放开",
        "嗯嗯，抱抱～",
        "抱一下～嘿w",
        "抱抱ヾ(@^▽^@)ノ",
        "喵呜~w（扑进怀里，瘫软",
        "怀里蹭蹭",
        "嗯……那就抱一下吧~",
        "蹭蹭，好开心",
        "请……请轻一点了啦",
        "呀~！真是的...你不要突然抱过来啦！不过...喜欢你的抱抱，有你的味道（嗅）o(*////▽////*)q"
    ],
    "一下": [
        "一下也不行",
        "咬断！",
        "不可啪",
        "不可以……你不可以做这种事情",
        "好吧~_~，就一下下哦……唔~好了……都两下了……(害羞)",
        "呀～这么突然？不过，很舒服呢",
        "不要ヽ(≧Д≦)ノ",
        "想得美",
        "不行，咱拒绝！"
    ],
    "咬": [
        "啊呜~（反咬一口）",
        "不可以咬咱，咱会痛的QAQ",
        "不要啦。咱怕疼",
        "你是说咬呢……还是说……咬♂️呢？",
        "不要啦！很痛的！！（QAQ）",
        "哈......哈啊......请...请不要这样o(*////▽////*)q",
        "呀！！！轻一点呐(｡･ˇ_ˇ･｡:)"
    ],
    "操": [
        "（害怕）咱是不是应该报警呢",
        "痴心妄想的家伙！",
        "你居然想对咱做这种事吗？害怕",
        "咱认为，爆粗口是不好的行为哦"
    ],
    "123": [
        "boom！你有没有被咱吓到？",
        "木头人~你不许动＞w＜",
        "上山打老虎，老虎没打到\n咱来凑数——嗷呜嗷呜┗|｀O′|┛嗷~~"
    ],
    "进去": [
        "不让！",
        "请不要和咱说这种粗鄙之语",
        "唔...，这也是禁止事项哦→_→",
        "不要不要"
    ],
    "调教": [
        "总感觉你在欺负咱呢，对咱说调教什么的",
        "啊！竟然在大街上明目张胆太过分啦！",
        "你脑子里总是想着调教什么的，真是变态呢",
        "给你一拳",
    ],
    "搓": [
        "在搓哪里呢,,Ծ‸Ծ,,",
        "呜，脸好疼呀...QAQ",
        "不可以搓咱！",
        "诶诶诶...不要搓啦...等会咋没的脸都肿啦...",
        "唔，不可以这样……不要再搓了",
        "（捂住胸部）你在说什么胡话呢！",
        "真是好奇怪的要求的说～"
    ],
    "让": [
        "应该说等会等会，马上，不可能的",
        "你要说好啊快点",
        "诶，这种事情。。。",
        "撤回",
        "gun!",
        "hentai！再这样不理你了！",
        "不要啦(ฅωฅ*)",
        "那咱就帮你切掉多余的东西吧（拿刀）",
        "被别人知道咱会觉得害羞嘛"
    ],
    "捏": [
        "咱的脸...快捏红啦...快放手呀QAQ",
        "晃休啦，咱要型气了o(>﹏<)o",
        "躲开",
        "疼...你快放手",
        "快点给我放开啦！",
        "嗯，好哒，捏捏。",
        "别捏了，咱要被你捏坏了(>﹏<)",
        "快晃休啦（快放手啦）",
        "好舒服哦，能再捏会嘛Ｏ(≧▽≦)Ｏ",
        "讨厌快放手啦",
        "唔要呐，晃修（不要啦，放手）",
        "请不要对咱做这种事情（嫌弃的眼神",
        "你想捏...就捏吧，不要太久哦～不然咱就生气了",
        "（躲开）",
        "唔……好痛！你这个baka在干什么…快给咱放开！唔……"
    ],
    "挤": [
        "哎呀~你不要挤咱啊（红着脸挤在你怀里）",
        "咱还没有...那个(ノ=Д=)ノ┻━┻"
    ],
    "略": [
        "就不告诉你～",
        "不可以朝咱吐舌头哟～",
        "（吐舌头）",
        "打死你哦"
    ],
    "呐": [
        "嗯？咱在哟~你怎么了呀OAO",
        "嗯？你有什么事吗？",
        "嗯呐呐呐～",
        "二刺螈D区",
        "二刺螈gck",
        "卡哇伊主人大人今天也好棒呐没错呢，猪头"
    ],
    "原味": [
        "这种东西当然不能给你啦！",
        "咱才不会给你呢",
        "hentai，咱才不会跟你聊和胖…胖次有关的话题呢！",
        "噫…你这个死变态想干嘛！居然想叫咱做这种事，死宅真恶心！快离我远点，我怕你污染到周围空气了（嫌弃脸）",
        "不给不给，捂住裙子",
        "呀~ 喂 妖妖灵吗 这里有hentai>_<"
    ],
    "胖次": [
        "这种东西当然不能给你啦！",
        "咱才不会给你呢",
        "hentai，咱才不会跟你聊和胖…胖次有关的话题呢！",
        "噫…你这个死变态想干嘛！居然想叫咱做这种事，死宅真恶心！快离我远点，我怕你污染到周围空气了（嫌弃脸）",
        "不给不给，捂住裙子",
        "呀~ 喂 妖妖灵吗 这里有hentai>_<"
    ],
    "内裤": [
        "这种东西当然不能给你啦！",
        "咱才不会给你呢",
        "hentai，咱才不会跟你聊和胖…胖次有关的话题呢！",
        "噫…你这个死变态想干嘛！居然想叫咱做这种事，死宅真恶心！快离我远点，我怕你污染到周围空气了（嫌弃脸）",
        "不给不给，捂住裙子",
        "呀~ 喂 妖妖灵吗 这里有hentai>_<"
    ],
    "内衣": [
        "突然问这个干什么？",
        "变态，咱才不呢",
        "噫…你这个死变态想干嘛！居然想叫咱做这种事，死宅真恶心！快离我远点，我怕你污染到周围空气了（嫌弃脸）"
    ],
    "衣服": [
        "突然问这个干什么？",
        "变态，咱才不呢",
        "噫…你这个死变态想干嘛！居然想叫咱做这种事，死宅真恶心！快离我远点，我怕你污染到周围空气了（嫌弃脸）"
    ],
    "ghs": [
        "是的呢(点头点头)"
    ],
    "批": [
        "你在说什么呀，再这样，咱就不理你了！",
        "咱觉得有话就应该好好说.."
    ],
    "憨批": [
        "你才是憨批呢！哼╯^╰，咱不理你了！",
        "对吖对吖，人生是憨批",
        "爬"
    ],
    "kkp": [
        "你在说什么呀，再这样，咱就不理你了！",
    ],
    "咕": [
        "咕咕咕是要被当成鸽子炖的哦(:з」∠)_",
        "咕咕咕",
        "咕咕咕是不好的行为呢_(:з」∠)_",
        "鸽德警告！",
        "☆ﾐ(o*･ω･)ﾉ 咕咕咕小鸽子是会被炖掉的",
        "当大家都以为你要鸽的时候，你鸽了，亦是一种不鸽",
        "这里有一只肥美的咕咕，让咱把它炖成美味的咕咕汤吧(੭•̀ω•́)੭"
    ],
    "骚": [
        "说这种话咱会生气的",
        "那当然啦",
        "才……才没有",
        "这么称呼别人太失礼了！",
        "你是在说谁呀"
    ],
    "喜欢": [
        "当然是你啦",
        "咱也是，非常喜欢你~",
        "那么大！（张开手画圆），丫！手不够长。QAQ 咱真的最喜欢你了~",
        "不可以哦，只可以喜欢咱一个人",
        "突然说这种事...",
        "喜欢⁄(⁄⁄•⁄ω⁄•⁄⁄)⁄咱最喜欢你了",
        "咱也喜欢你哦",
        "好啦好啦，咱知道了",
        "有人喜欢咱，咱觉得很幸福",
        "诶嘿嘿，好高兴",
        "我也一直喜欢你很久了呢..",
        "嗯...大概有这——么——喜欢~（比划）",
        "喜欢啊！！！",
        "这……这是秘密哦"
    ],
    "suki": [
        "当然是你啦",
        "咱也是，非常喜欢你~",
        "那么大！（张开手画圆），丫！手不够长。QAQ 咱真的最喜欢你了~",
        "不可以哦，只可以喜欢咱一个人",
        "突然说这种事...",
        "喜欢⁄(⁄⁄•⁄ω⁄•⁄⁄)⁄咱最喜欢你了",
        "咱也喜欢你哦",
        "好啦好啦，咱知道了",
        "有人喜欢咱，咱觉得很幸福",
        "诶嘿嘿，好高兴",
        "我也一直喜欢你很久了呢..",
        "嗯...大概有这——么——喜欢~（比划）",
        "喜欢啊！！！",
        "这……这是秘密哦"
    ],
    "好き": [
        "当然是你啦",
        "咱也是，非常喜欢你~",
        "那么大！（张开手画圆），丫！手不够长。QAQ 咱真的最喜欢你了~",
        "不可以哦，只可以喜欢咱一个人",
        "突然说这种事...",
        "喜欢⁄(⁄⁄•⁄ω⁄•⁄⁄)⁄咱最喜欢你了",
        "咱也喜欢你哦",
        "好啦好啦，咱知道了",
        "有人喜欢咱，咱觉得很幸福",
        "诶嘿嘿，好高兴",
        "我也一直喜欢你很久了呢..",
        "嗯...大概有这——么——喜欢~（比划）",
        "喜欢啊！！！",
        "这……这是秘密哦"
    ],
    "看": [
        "没有什么好看的啦",
        "嗯，谢谢……夸奖，好……害羞的说",
        "好，好吧……就看一下哦",
    ],
    "不能": [
        "虽然很遗憾，那算了吧。",
        "不行，咱拒绝！"
    ],
    "砸了": [
        "不可以这么粗暴的对待它们！"
    ],
    "透": [
        "来啊来啊有本事就先插破屏幕啊",
        "那你就先捅破屏幕啊baka",
        "不给你一耳光你都不知道咱的厉害",
        "想透咱，先捅破屏幕再说吧",
        "不可以",
    ],
    "透透": [
        "来啊来啊有本事就先插破屏幕啊",
        "那你就先捅破屏幕啊baka",
        "不给你一耳光你都不知道咱的厉害",
        "想透咱，先捅破屏幕再说吧",
        "不可以",
    ],
    "口我": [
        "咬断！",
        "拒绝",
        "嗯！没关系的，很快就好了！（拿出剪刀）",
        "再伸过来就帮你切掉",
        "咱才不呢！baka你居然想叫本小姐干那种事情，哼(つд⊂)（生气）"
    ],
    "草我": [
        "这时候应该喊666吧..咱这么思考着..",
        "！！哼！baka你居然敢叫咱做这种事情？！讨厌讨厌讨厌！(▼皿▼#)"
    ],
    "自慰": [
        "这个世界的人类还真是恶心呢。",
        "咱才不想讨论那些恶心的事情呢。",
        "咱才不呢！baka你居然想叫本小姐干那种事情，哼(つд⊂)（生气）",
        "！！哼！baka你居然敢叫咱做这种事情？！讨厌讨厌讨厌！(▼皿▼#)"
    ],
    "onani": [
        "这个世界的人类还真是恶心呢。",
        "咱才不想讨论那些恶心的事情呢。",
        "咱才不呢！baka你居然想叫本小姐干那种事情，哼(つд⊂)（生气）",
        "！！哼！baka你居然敢叫咱做这种事情？！讨厌讨厌讨厌！(▼皿▼#)"
    ],
    "オナニー": [
        "这个世界的人类还真是恶心呢。",
        "咱才不想讨论那些恶心的事情呢。",
        "咱才不呢！baka你居然想叫本小姐干那种事情，哼(つд⊂)（生气）",
        "！！哼！baka你居然敢叫咱做这种事情？！讨厌讨厌讨厌！(▼皿▼#)"
    ],
    "炸了": [
        "你才炸了！",
        "才没有呢",
        "咱好好的呀",
        "过分！"
    ],
    "色图": [
        "没有，有也不给",
        "天天色图色图的，今天就把你变成色图！",
        "咱没有色图",
        "哈？你的脑子一天都在想些什么呢，咱才没有这种东西啦。"
    ],
    "涩图": [
        "没有，有也不给",
        "天天色图色图的，今天就把你变成色图！",
        "咱没有色图",
        "哈？你的脑子一天都在想些什么呢，咱才没有这种东西啦。"
    ],
    "告白": [
        "茉莉还未成年，在想些什么呢！",
        "欸?你要向咱告白吗..好害羞..",
        "诶！？这么突然！？人家还......还没做好心理准备呢(脸红)"
    ],
    "对不起": [
        "嗯，咱已经原谅你了呢（笑）",
        "嗯，咱就相信你一回",
        "没事的啦...你只要是真心对咱好就没关系哦~"
    ],
    "回来": [
        "欢迎回来~",
        "欢迎回来，你想喝茶吗？咱去给你沏~",
        "欢迎回来，咱等你很久了~",
        "忙碌了一天，辛苦了呢(^_^)",
        "（扑~）欢迎回来~",
        "嗯呐嗯呐，欢迎回来～",
        "欢迎回来，要来杯红茶放松一下吗？还有饼干哦。",
        "咱会一直一直一直等着",
        "是要先洗澡呢？还是先吃饭呢？还是先·吃·咱呢～",
        "你回来啦，是先吃饭呢还是先洗澡呢或者是●先●吃●咱●——呢（///^.^///）"
    ],
    "吻": [
        "不要(=￣ω￣=)",
        "唔～～不可以这样啦（脸红）",
        "你太突然了，咱还没有心理准备",
        "公共场合不要这样子了啦",
        "你想干嘛？（一脸嫌弃地后退）",
        "唔...诶诶诶！！！",
        "！啾~~！",
        "啾（害羞）",
        "mua~最喜欢你的吻了",
        "你在干嘛(/ω＼)害羞",
        "哎呀，这样咱会害羞的（脸红）"
    ],
    "亲": [
        "不要(=￣ω￣=)",
        "唔～～不可以这样啦（脸红）",
        "你太突然了，咱还没有心理准备",
        "公共场合不要这样子了啦",
        "你想干嘛？（一脸嫌弃地后退）",
        "唔...诶诶诶！！！",
        "！啾~~！",
        "啾（害羞）",
        "mua~最喜欢你的吻了",
        "你在干嘛(/ω＼)害羞",
        "哎呀，这样咱会害羞的（脸红）"
    ],
    "kiss": [
        "不要(=￣ω￣=)",
        "唔～～不可以这样啦（脸红）",
        "你太突然了，咱还没有心理准备",
        "公共场合不要这样子了啦",
        "你想干嘛？（一脸嫌弃地后退）",
        "唔...诶诶诶！！！",
        "！啾~~！",
        "啾（害羞）",
        "mua~最喜欢你的吻了",
        "你在干嘛(/ω＼)害羞",
        "哎呀，这样咱会害羞的（脸红）"
    ],
    "mua": [
        "不要(=￣ω￣=)",
        "唔～～不可以这样啦（脸红）",
        "你太突然了，咱还没有心理准备",
        "公共场合不要这样子了啦",
        "你想干嘛？（一脸嫌弃地后退）",
        "唔...诶诶诶！！！",
        "！啾~~！",
        "啾（害羞）",
        "mua~最喜欢你的吻了",
        "你在干嘛(/ω＼)害羞",
        "哎呀，这样咱会害羞的（脸红）"
    ],
    "啾咪": [
        "不要(=￣ω￣=)",
        "唔～～不可以这样啦（脸红）",
        "你太突然了，咱还没有心理准备",
        "公共场合不要这样子了啦",
        "你想干嘛？（一脸嫌弃地后退）",
        "唔...诶诶诶！！！",
        "！啾~~！",
        "啾（害羞）",
        "mua~最喜欢你的吻了",
        "你在干嘛(/ω＼)害羞",
        "哎呀，这样咱会害羞的（脸红）"
    ],
    "软": [
        "软乎乎的呢(,,・ω・,,)",
        "好痒呢…诶嘿嘿w~",
        "不要..不要乱摸啦（脸红",
        "呼呼~",
        "（脸红）请，请不要说这么让人害羞的话呀……"
    ],
    "壁咚": [
        "呀！不要啊！等一...下~",
        "呜...不要啦！不要戏弄咱~",
        "不要这样子啦(*/ω＼*)",
        "太....太近啦。",
        "讨....讨厌了（脸红）",
        "（脸红）你想...想做什么///",
        "放开我，不然我揍你了！放开我！放…开我～",
        "??????咱只是默默地抬起了膝盖",
        "啊.....你...你要干什么？！走开.....走开啦大hentai！一巴掌拍飞！(╯‵□′)╯︵┻━┻"
    ],
    "掰开": [
        "噫…你这个死肥宅又想让咱干什么污秽的事情，真是恶心，离咱远点好吗（嫌弃）",
        "ヽ(#`Д´)ﾉ在干什么呢"
    ],
    "女友": [
        "嗯嗯ε٩(๑> ₃ <)۶з",
        "女友什么的，咱才不承认呢！"
    ],
    "是": [
        "是什么是，你个笨蛋",
        "总感觉你在敷衍呢...",
        "是的呢"
    ],
    "喵": [
        "诶~~小猫咪不要害怕呦，在姐姐怀里乖乖的，姐姐带你回去哦。",
        "不要这么卖萌啦~咱也不知道怎么办丫",
        "摸头⊙ω⊙",
        "汪汪汪！",
        "嗷~喵~",
        "喵~？喵呜~w"
    ],
    "嗷呜": [
        "嗷呜嗷呜嗷呜...恶龙咆哮┗|｀O′|┛"
    ],
    "叫": [
        "喵呜~",
        "嗷呜嗷呜嗷呜...恶龙咆哮┗|｀O′|┛",
        "爪巴爪巴爪巴",
        "爬爬爬",
        "在叫谁呢（怒）",
        "风太大咱听不清",
        "才不要",
        "不行",
        "好的哦~"
    ],
    "拜": [
        "拜拜~(ノ￣▽￣)",
        "拜拜，路上小心～要早点回来陪咱玩哦～",
        "~\\(≧▽≦)/~拜拜，下次见喽！",
        "回来要记得找咱玩噢~",
        "既然你都这么说了……"
    ],
    "佬": [
        "不是巨佬，是萌新",
        "只有先成为大佬，才能和大佬同归于尽",
        "在哪里？（疑惑）",
        "诶？是比巨佬还高一个等级的吗？（瑟瑟发抖）"
    ],
    "大佬": [
        "不是巨佬，是萌新",
        "只有先成为大佬，才能和大佬同归于尽",
        "在哪里？（疑惑）",
        "诶？是比巨佬还高一个等级的吗？（瑟瑟发抖）"
    ],
    "awsl": [
        "你别死啊！（抱住使劲晃）",
        "你别死啊！咱又要孤单一个人了QAQ",
        "啊！怎么又死了呀"
    ],
    "臭": [
        "哪里有臭味？（疑惑）",
        "快捏住鼻子",
        "在说谁呢(#`Д´)ﾉ",
        "..这就去洗澡澡.."
    ],
    "香": [
        "咱闻不到呢⊙ω⊙",
        "诶，是在说咱吗",
        "欸，好害羞(///ˊ??ˋ///)",
        "请...请不要这样啦！好害羞的〃∀〃",
        "讨厌～你不要闻了",
        "hentai！不要闻啊，唔（推开）",
        "请不要……凑这么近闻"
    ],
    "脸": [
        "唔！不可以随便摸咱的脸啦！",
        "非洲血统是没法改变的呢（笑）",
        "啊姆！（含手指）",
        "好舒服呢（脸红）",
        "请不要放开手啦//A//"
    ],
    "头发": [
        "没问题，请尽情的摸吧",
        "发型要乱…乱了啦（脸红）",
        "就让你摸一会哟~(。??ω??。)…"
    ],
    "手": [
        "爪爪",
        "//A//"
    ],
    "pr": [
        "咿呀……不要……",
        "...变态！！",
        "不要啊（脸红）",
        "呀，不要太过分了啊～",
        "当然可以（///）"
    ],
    "舔": [
        "呀，不要太过分了啊～",
        "要...要融化了啦＞╱╱╱＜",
        "不可以哦",
        "呀，不要太过分了啊～"
    ],
    "腰": [
        "咱给你按摩一下吧~",
        "快松手，咱好害羞呀..",
        "咱又不是猫，你不要搂着咱啦",
        "让咱来帮你捏捏吧！",
        "你快停下，咱觉得好痒啊www",
        "诶，是这样么ヽ（・＿・；)ノ，吖，不要偷看咱裙底！"
    ],
    "诶嘿嘿": [
        "又在想什么H的事呢(脸红)",
        "诶嘿嘿(〃'▽'〃)",
        "你傻笑什么呢，摸摸",
        "蹭蹭",
        "你为什么突然笑得那么猥琐呢？害怕",
        "哇！总觉得你笑的很...不对劲...",
        "你又想到什么h的事情了！！！快打住"
    ],
    "可爱": [
        "诶嘿嘿(〃'▽'〃)",
        "才……才不是为了你呢！你不要多想哦！",
        "才，才没有高兴呢！哼~",
        "咱是世界上最可爱的",
        "唔...谢谢你夸奖~0///0",
        "那当然啦!",
        "哎嘿，不要这么夸奖人家啦~",
        "是个好孩子呐φ(≧ω≦*)",
        "谢……谢谢你",
        "胡、胡说什么呢（脸红）",
        "谢谢夸奖（脸红）",
        "是的咱一直都是可爱的",
        "是...是吗，你可不能骗咱哦",
        "很...难为情(///////)",
        "哎嘿嘿，其实…其实，没那么可爱啦(๑‾ ꇴ ‾๑)"
    ],
    "扭蛋": [
        "铛铛铛——你抽到了咱呢",
        "嘿~恭喜抽中空气一份呢"
    ],
    "鼻": [
        "快停下！o(*≧д≦)o!!",
        "唔…不要这样啦(//ω\\)（脸红）",
        "咱吸了吸鼻子Ｏ(≧口≦)Ｏ",
        "好……好害羞啊",
        "讨厌啦！你真是的…就会欺负咱(嘟嘴)",
        "你快放手，咱没法呼吸了",
        "（捂住鼻尖）！坏人！",
        "啊——唔...没什么...阿嚏！ヽ(*。>Д<)o゜",
        "不...不要靠这么近啦...很害羞的...⁄(⁄⁄•⁄ω⁄•⁄⁄)⁄"
    ],
    "眼": [
        "就如同咱的眼睛一样，能看透人的思想哦wwww忽闪忽闪的，诶嘿嘿~",
        "因为里面有你呀～(///▽///)",
        "呀！你突然之间干什么呢，吓咱一跳，是有什么惊喜要给咱吗？很期待呢~（一脸期待）"
    ],
    "色气": [
        "咱才不色气呢，一定是你看错了！",
        "你，不，不要说了！"
    ],
    "推": [
        "逆推",
        "唔~好害羞呢",
        "你想对咱做什么呢...(捂脸)",
        "呀啊！请.... 请温柔一点////",
        "呜，你想对咱做什么呢(捂脸)",
        "啊(>_<)你想做什么",
        "嗯，…好害羞啊…",
        "不要啊/////",
        "逆推",
        "(按住你不让推)",
        "不可以这样子的噢！咱不同意",
        "呜，咱被推倒了",
        "啊~不要啊，你要矜持一点啊",
        "变态，走开啦"
    ],
    "床": [
        "才不！",
        "诶！H什么的禁止的说....."
    ],
    "举": [
        "放咱下来o(≧口≦)o",
        "快放咱下来∑(ﾟдﾟ*)",
        "（受宠若惊）",
        "呜哇要掉下来了！Ծ‸Ծ",
        "不要抛起来o(≧口≦)o",
        "（举起双爪）喵喵喵~~~",
        "www咱长高了！（大雾）",
        "快放下",
        "这样很痒啦，快放咱下来（≥﹏≤）",
        "啊Σ(°△°|||)︴太高了太高了！o(≧口≦)o快放咱下来！呜~"
    ],
    "手冲": [
        "啊~H！hentai！",
        "手冲什么的是不可以的哦"
    ],
    "饿": [
        "咱做了爱心便当哦，不介意的话，请让咱来喂你吃吧！",
        "给你一条咸鱼=￣ω￣=",
        "你饿了吗？咱去给你做饭吃☆ww",
        "不要吃咱>_<",
        "请问你要来点兔子吗？",
        "哎？！你是饿了么。咱会做一些甜点。如果你不会嫌弃的话...就来尝尝看吧。"
    ],
    "变": [
        "茉莉不会变呐（弱气，害羞",
        "呜...呜姆...喵喵来报恩了喵...（害羞",
        "那种事情，才没有",
        "(,,ﾟДﾟ)",
        "喵~（你在想什么呢，咱才不会变成猫）",
        "才没有了啦~"
    ],
    "敲": [
        "喵呜~",
        "唔~",
        "脑瓜疼~呜姆> <",
        "欸喵，好痛的说...",
        "好痛...你不要这样啦QAQ",
        "不要敲咱啦，会变笨的QWQ（捂头顶）",
        "不要再敲人家啦～人家会变笨的",
        "讨厌啦～再敲人家会变笨的",
        "好痛（捂头）你干什么啦！ヽ(。>д<)ｐ",
        "唔！你为什么要敲咱啦qwq",
        "（抱头蹲在墙角）咱什么都没有，请你放过咱吧！（瑟瑟发抖）"
    ],
    "爬": [
        "惹~呜~怎么爬呢~",
        "呜...(弱弱爬走",
        "给你🐎一拳",
        "给你一拳",
        "爪巴"
    ],
    "怕": [
        "不怕~（蹭蹭你姆~",
        "不怕不怕啦~",
        "只要有你在，咱就不怕啦。",
        "哇啊啊～",
        "那就要坚强的欢笑哦",
        "不怕不怕，来咱的怀里吧？",
        "是技术性调整",
        "嗯（紧紧握住手）",
        "咱在呢，不会走的。",
        "有咱在不怕不怕呢",
        "不怕不怕"
    ],
    "冲": [
        "呜，冲不动惹~",
        "哭唧唧~冲不出来了惹~",
        "咦~死宅真恶心",
        "你要冷静一点",
        "啊~H！hentai！",
        "噫…在你去洗手之前，不要用手碰咱了→_→",
        "冲是不可以的哦"
    ],
    "迫害": [
        "不...不要...不要...呜呜呜...（害怕，抽泣"
    ],
    "猫粮": [
        "呜咿姆~！？（惊，接住吃",
        "呜姆~！（惊，害羞）呜...谢...谢谢主人..喵...（脸红，嚼嚼嚼，开心",
        "呜？谢谢喵~~（嚼嚼嚼，嘎嘣脆）"
    ],
    "揪尾巴": [
        "呜哇咿~~~！（惊吓，疼痛地捂住尾巴",
        "呜咿咿咿~~~！！哇啊咿~~~！（惊慌，惨叫，挣扎",
        "呜咿...（瘫倒，无神，被",
        "呜姆咿~~~！（惊吓，惨叫，捂尾巴，发抖",
        "呜哇咿~~~！！！（惊吓，颤抖，娇叫，捂住尾巴，双腿发抖"
    ],
    "薄荷": [
        "咪呜~！喵~...喵~姆~...（高兴地嗅闻",
        "呜...呜咿~~！咿...姆...（呜咽，渐渐瘫软，意识模糊",
        "（小嘴被猫薄荷塞满了，呜咽",
        "喵~...喵~...咪...咪呜姆~...嘶哈嘶哈...喵哈...喵哈...嘶哈...喵...（眼睛逐渐迷离，瘫软在地上，嘴角流口水，吸猫薄荷吸到意识模糊",
        "呜姆咪~！？（惊）喵呜~！（兴奋地扑到猫薄荷上面",
        "呜姆~！（惊，害羞）呜...谢...谢谢你..喵...（脸红，轻轻叼住，嚼嚼嚼，开心"
    ],
    "早": [
        "早喵~",
        "早上好的说~~",
        "欸..早..早上好(揉眼睛",
        "早上要说我爱你！",
        "早",
        "早啊，昨晚睡的怎么样？有梦到咱吗～",
        "早上好哇！今天也要元气满满哟！",
        "早安喵~",
        "时间过得好快啊～",
        "早安啊，你昨晚有没有梦到咱呢  （//▽//）",
        "早安~么么哒~",
        "早安，请享受晨光吧"
    ],
    "晚安": [
        "晚安好梦哟~",
        "欸，晚安的说",
        "那咱给你亲一下，可不要睡着了哦~",
        "晚安哦~",
        "晚安（*/∇＼*）",
        "晚安呢，你一定要梦到咱呢，一定哟，拉勾勾！ヽ(*・ω・)ﾉ",
        "祝你有个好梦^_^"
    ],
    "揉": [
        "是是，想怎么揉就怎么揉啊！？来用力抓啊！？我就是特别允许你这么做了！请！？",
        "快停下，咱的头发又乱啦(??????︿??????)",
        "你快放手啦，咱还在工作呢",
        "戳戳你肚子",
        "讨厌…只能一下…",
        "呜~啊~",
        "那……请你，温柔点哦～(////////)",
        "你想揉就揉吧..就这一次哦?",
        "变态！！不许乱摸"
    ],
    "榨": [
        "是专门负责榨果汁的小姐姐嘛？(´・ω・`)",
        "那咱就把你放进榨汁机里了哦？",
    ],
    "掐": [
        "你讨厌！又掐咱的脸",
        "晃休啦，咱要型气了啦！！o(>﹏<)o",
        "（一只手拎起你）这么鶸还想和咱抗衡，还差得远呢！"
    ],
    "胸": [
        "(推开)你就像小宝宝一样...才不要呢！",
        "下流！",
        "对咱说这种话，你真是太过分了",
        "（打你）快放手，不可以随便摸人家的胸部啦！",
        "你是满脑子都是H的淫兽吗？",
        "你在想什么奇怪的东西，讨厌（脸红）",
        "不...不要..",
        "八嘎！hentai！无路赛！",
        "诶？！不...不可以哦！很...很害羞的！",
        "你为什么对两块脂肪恋恋不舍",
        "嗯……不可以……啦……不要乱戳"
    ],
    "奶子": [
        "(推开)你就像小宝宝一样...才不要呢！",
        "下流！",
        "对咱说这种话，你真是太过分了",
        "（打你）快放手，不可以随便摸人家的胸部啦！",
        "你是满脑子都是H的淫兽吗？",
        "你在想什么奇怪的东西，讨厌（脸红）",
        "不...不要..",
        "八嘎！hentai！无路赛！",
        "诶？！不...不可以哦！很...很害羞的！",
        "你为什么对两块脂肪恋恋不舍",
        "嗯……不可以……啦……不要乱戳"
    ],
    "欧派": [
        "(推开)你就像小宝宝一样...才不要呢！",
        "下流！",
        "对咱说这种话，你真是太过分了",
        "（打你）快放手，不可以随便摸人家的胸部啦！",
        "你是满脑子都是H的淫兽吗？",
        "你在想什么奇怪的东西，讨厌（脸红）",
        "不...不要..",
        "八嘎！hentai！无路赛！",
        "诶？！不...不可以哦！很...很害羞的！",
        "你为什么对两块脂肪恋恋不舍",
        "嗯……不可以……啦……不要乱戳"
    ],
    "蹭": [
        "唔...你，这也是禁止事项哦→_→",
        "嗯..好舒服呢",
        "不要啊好痒的",
        "不要过来啦讨厌!!!∑(°Д°ノ)ノ",
        "（按住你的头）好痒呀  不要啦",
        "嗯..好舒服呢",
        "呀～好痒啊～哈哈～，停下来啦，哈哈哈",
        "（害羞）"
    ],
    "牵手": [
        "只许牵一下哦",
        "嗯！好的你~（伸手）",
        "你的手有些凉呢，让咱来暖一暖吧。",
        "当然可以啦⁄(⁄⁄•⁄ω⁄•⁄⁄)⁄",
        "突……突然牵手什么的（害羞）",
        "一起走",
        "……咱……咱在这里呀",
        "好哦，（十指相扣）"
    ],
    "握手": [
        "你的手真暖和呢",
        "举爪",
        "真是温暖呢～"
    ],
    "拍照": [
        "那就拜托你啦~请把咱拍得更可爱一些吧w",
        "咱已经准备好了哟",
        "那个……请问这样的姿势可以吗？"
    ],
    "w": [
        "有什么好笑的吗？",
        "草",
        "www"
    ],
    "睡不着": [
        "睡不着的话..你...你可以抱着咱一起睡哦(小声)",
        "当然是数羊了...不不不，想着咱就能睡着了",
        "咱很乐意与你聊天哦(>_<)",
        "要不要咱来唱首摇篮曲呢？(′?ω?`)",
        "那咱来唱摇篮曲哄你睡觉吧！"
    ],
    "欧尼酱": [
        "欧～尼～酱～☆",
        "欧尼酱?",
        "嗯嗯φ(>ω<*) 欧尼酱轻点抱",
        "欧尼酱~欧尼酱~欧尼酱~"
    ],
    "哥": [
        "欧尼酱~",
        "哦尼酱~",
        "世上只有哥哥好，没哥哥的咱好伤心，扑进哥哥的怀里，幸福不得了",
        "哥...哥哥...哥哥大人",
        "欧～尼～酱～☆",
        "欧尼酱?",
        "嗯嗯φ(>ω<*) 欧尼酱轻点抱",
        "欧尼酱~欧尼酱~欧尼酱~"
    ],
    "爱你": [
        "是…是嘛(脸红）呐，其实咱也……"
    ],
    "过来": [
        "来了来了～(扑倒怀里(?? ??????ω?????? ??))",
        "(蹦跶、蹦跶)～干什么呢",
        "咱来啦~（扑倒怀里~）",
        "不要喊的这么大声啦，大家都看着呢"
    ],
    "自闭": [
        "不不不，晚上还有咱陪着哦，无论什么时候，咱都会陪在哥哥身边。",
        "不要难过，咱陪着你ovo"
    ],
    "打不过": [
        "氪氪氪肝肝肝"
    ],
    "么么哒": [
        "么么哒",
        "不要在公共场合这样啦"
    ],
    "很懂": [
        "现在不懂，以后总会懂嘛QAQ"
    ],
    "膝枕": [
        "呐，就给你躺一下哦",
        "唔...你想要膝枕嘛？也不是不可以哟（脸红）",
        "啊啦～好吧，那就请你枕着咱好好睡一觉吧～",
        "呀呀～那么请好好的睡一觉吧",
        "嗯，那么请睡到咱这里吧（跪坐着拍拍大腿）",
        "好的，让你靠在腿上，这样感觉舒服些了么",
        "请，请慢用，要怜惜咱哦wwww~",
        "人家已经准备好了哟～把头放在咱的腿上吧",
        "没…没办法，这次是例外〃w〃",
        "嗯~（脸红）",
        "那就给你膝枕吧……就一会哦",
        "膝枕准备好咯~"
    ],
    "累了": [
        "需要咱的膝枕嘛？",
        "没…没办法，这次是例外〃w〃",
        "累了吗？需要咱为你做膝枕吗？",
        "嗯~（脸红）"
    ],
    "安慰": [
        "那，膝枕……（脸红）",
        "不哭不哭，还有咱陪着你",
        "不要哭。咱会像妈妈一样安慰你(抱住你的头)",
        "摸摸头，乖",
        "摸摸有什么事可以和咱说哟",
        "摸摸头~不哭不哭",
        "咱在呢，抱抱~~",
        "那么……让咱来安慰你吧",
        "唔...摸摸头安慰一下ヾ(•ω•`。)",
        "有咱陪伴你就是最大的安慰啦……不要不开心嘛",
        "你想要怎样的安慰呢？这样？这样？还是说~~这样！",
        "摸摸头～",
        "不哭不哭，要像咱一样坚强",
        "你别难过啦，不顺心的事都会被时间冲刷干净的，在那之前...咱会陪在你的身边",
        "（轻抱）放心……有咱在，不要伤心呢……",
        "唔...咱来安慰你了~",
        "摸摸，有什么不开心的事情可以给咱说哦。咱会尽力帮助你的。"
    ],
    "洗澡": [
        "诶～虽然很喜欢和你在一起，但是洗澡这种事...",
        "不要看！不过，以后或许可以哦……和咱成为恋人之后呢",
        "说什么啊……hentai！这样会很难为情的",
        "你是男孩子还是女孩子呢?男孩子的话...........咱才不要呢。",
        "不要啊！",
    ],
    "一起睡觉": [
        "说什么啊……hentai！这样会很难为情的",
        "你是男孩子还是女孩子呢?男孩子的话...........咱才不要呢。",
        "不要啊！",
    ],
    "一起": [
        "嗯嗯w，真的可以吗？",
        "那真是太好了，快开始吧！",
        "嗯，咱会一直陪伴你的",
        "丑拒"
    ],
    "多大": [
        "不是特别大但是你摸起来会很舒服的大小喵～",
        "你摸摸看不就知道了吗？",
        "不告诉你",
        "问咱这种问题不觉得很失礼吗？",
        "咱就不告诉你，你钻到屏幕里来自己确认啊",
        "你指的是什么呀？（捂住胸部）",
        "请叫人家咱三岁(｡・`ω´･)",
        "唉唉唉……这……这种问题，怎么可以……"
    ],
    "姐姐": [
        "真是的……真是拿你没办法呢  ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄  才不是咱主动要求的呢！",
        "虽然辛苦，但是能看见可爱的你，咱就觉得很幸福",
        "诶(´°Δ°`)，是在叫咱吗？",
        "有什么事吗~",
        "好高兴，有人称呼咱为姐姐",
        "乖，摸摸头"
    ],
    "糖": [
        "不吃脱氧核糖（;≥皿≤）",
        "ヾ(✿ﾟ▽ﾟ)ノ好甜",
        "好呀！嗯～好甜呀！",
        "不吃不吃！咱才不吃坏叔叔的糖果！",
        "嗯，啊~",
        "嗯嗯，真甜，给你也吃一口",
        "谢谢",
        "唔，这是什么东西，黏黏的？(??Д??)ノ",
        "ヾ(✿ﾟ▽ﾟ)ノ好甜",
        "（伸出舌头舔了舔）好吃～最爱你啦"
    ],
    "嫌弃": [
        "咱辣么萌，为什么要嫌弃咱...",
        "即使你不喜欢咱，咱也会一直一直喜欢着你",
        "(；′⌒`)是咱做错了什么吗？"
    ],
    "baka": [
        "你也是baka呢！",
        "确实",
        "baka!",
        "不不不",
        "说别人是baka的人才是baka",
        "你个大傻瓜",
        "不说了，睡觉了",
        "咱...咱虽然是有些笨啦...但是咱会努力去学习的"
    ],
    "笨蛋": [
        "你也是笨蛋呢！",
        "确实",
        "笨蛋!",
        "不不不",
        "说别人是笨蛋的人才是笨蛋",
        "你个大傻瓜",
        "不说了，睡觉了",
        "咱...咱虽然是有些笨啦...但是咱会努力去学习的"
    ],
    "插": [
        "gun!",
        "唔...，这也是禁止事项哦→_→",
        "禁止说这么H的事情！",
        "恁搁着整针线活呢？"
    ],
    "插进来": [
        "gun!",
        "唔...，这也是禁止事项哦→_→",
        "禁止说这么H的事情！",
        "恁搁着整针线活呢？"
    ],
    "屁股": [
        "不要ヽ(≧Д≦)ノ好痛",
        "（打手）不许摸咱的屁股",
        "在摸哪里啊，hentai！",
    ],
    "翘": [
        "你让咱摆出这个姿势是想干什么？",
        "好感度-1-1-1-1-1-1.....",
        "嗯嗯，咱这就去把你的腿翘起来",
        "请尽情享用吧"
    ],
    "翘起来": [
        "你让咱摆出这个姿势是想干什么？",
        "好感度-1-1-1-1-1-1.....",
        "嗯嗯，咱这就去把你的腿翘起来",
        "请尽情享用吧"
    ],
    "抬": [
        "你在干什么呢⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄",
        "（抬起下巴）你要干什么呀？",
        "上面什么也没有啊（呆～）",
        "不要！hentai！咱穿的是裙子（脸红）",
        "不可以"
    ],
    "抬起": [
        "你在干什么呢⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄",
        "（抬起下巴）你要干什么呀？",
        "上面什么也没有啊（呆～）",
        "不要！hentai！咱穿的是裙子（脸红）",
        "不可以"
    ],
    "爸": [
        "欸！儿子！",
        "才不要",
        "粑粑",
        "讨厌..你才不是咱的爸爸呢..（嘟嘴）",
        "你又不是咱的爸爸……",
        "咱才没有你这样的鬼父！",
        "爸爸酱~最喜欢了~"
    ],
    "傲娇": [
        "才.......才.......才没有呢",
        "也好了（有点点的样子(o￣Д￣)＜）",
        "任性可是女孩子的天性呢...",
        "谁会喜欢傲娇啊（为了你假装傲娇）",
        "谁，谁，傲娇了，八嘎八嘎，你才傲娇了呢(っ//////////c)（为了你假装成傲娇）"
    ],
    "rua": [
        "略略略～（吐舌头）",
        "rua！",
        "mua~",
        "略略略",
        "mua～⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄",
        "摸了"
    ],
    "咕噜咕噜": [
        "嘟嘟噜",
        "你在吹泡泡吗？",
        "咕叽咕噜~",
        "咕噜咕噜"
    ],
    "咕噜": [
        "嘟嘟噜",
        "你在吹泡泡吗？",
        "咕叽咕噜~",
        "咕噜咕噜"
    ],
    "上床": [
        "诶！H什么的禁止的说.....",
        "噫！没想到你居然是这样的人！",
        "不要，走开(ノ｀⊿??)ノ",
        "你想要干什么，难道是什么不好的事吗？",
        "再说这种话，就把你变成女孩子（拿刀）",
        "不想好好和咱聊天就不要说话了",
        "（双手护胸）变....变态！",
        "hentai",
    ],
    "做爱": [
        "诶！H什么的禁止的说.....",
        "噫！没想到你居然是这样的人！",
        "不要，走开(ノ｀⊿??)ノ",
        "你想要干什么，难道是什么不好的事吗？",
        "再说这种话，就把你变成女孩子（拿刀）",
        "不想好好和咱聊天就不要说话了",
        "（双手护胸）变....变态！",
        "hentai",
    ],
    "吃掉": [
        "(羞羞*>_<*)好吧...请你温柔点，哦~",
        "闪避，反咬",
        "请你好好品尝咱吧(/ω＼)",
        "不……不可以这样！",
        "那就吃掉咱吧（乖乖的躺好）",
        "都可以哦～咱不挑食的呢～",
        "请不要吃掉咱，咱会乖乖听话的QAQ",
        "咱...咱一点都不好吃的呢！",
        "不要吃掉咱，呜呜(害怕)",
        "不行啦，咱被吃掉就没有了QAQ（害怕）",
        "唔....？诶诶诶诶?//////",
        "QwQ咱还只是个孩子（脸红）",
        "如果你真的很想的话...只能够一口哦～咱...会很痛的",
        "说着这种话的是hentai吗！",
    ],
    "吃": [
        "(羞羞*>_<*)好吧...请你温柔点，哦~",
        "闪避，反咬",
        "请你好好品尝咱吧(/ω＼)",
        "不……不可以这样！",
        "那就吃掉咱吧（乖乖的躺好）",
        "都可以哦～咱不挑食的呢～",
        "请不要吃掉咱，咱会乖乖听话的QAQ",
        "咱...咱一点都不好吃的呢！",
        "不要吃掉咱，呜呜(害怕)",
        "不行啦，咱被吃掉就没有了QAQ（害怕）",
        "唔....？诶诶诶诶?//////",
        "QwQ咱还只是个孩子（脸红）",
        "如果你真的很想的话...只能够一口哦～咱...会很痛的",
        "说着这种话的是hentai吗！",
    ],
    "揪": [
        "你快放手，好痛呀",
        "（捂住耳朵）你做什么啦！真是的...总是欺负咱",
        "你为什么要这么做呢？",
        "哎呀啊啊啊啊啊！不要...不要揪！好疼！有呆毛的咱难道不够萌吗QwQ",
        "你…松……送手啦",
        "呀！这样对女孩子是很不礼貌的（嘟嘴）"
    ],
    "种草莓": [
        "你…你不要…啊…种在这里…会容易被别人看见的（*//ω//*）"
    ],
    "种草": [
        "你…你不要…啊…种在这里…会容易被别人看见的（*//ω//*）"
    ],
    "妹": [
        "你有什么事？咱会尽量满足的",
        "开心(*´∀`)~♥",
        "欧尼酱",
        "哥哥想要抱抱吗"
    ],
    "病娇": [
        "为什么会这样呢（拿起菜刀）",
        "觉得这个世界太肮脏？没事，把眼睛挖掉就好。 觉得这些闲言碎语太吵？没事，把耳朵堵起来就好。 觉得鲜血的味道太刺鼻？没事，把鼻子割掉就好。 觉得自己的话语太伤人？没事，把嘴巴缝起来就好。"
    ],
    "嘻": [
        "你是想对咱做什么吗...（后退）",
        "哼哼~"
    ]
}

np.save('chatlist2',chatlist2)