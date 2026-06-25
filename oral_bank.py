import random

ORAL_TOPICS = [

{
    "picture":"assets/picture1.jpg",
    "question":"你看到同学乱丢垃圾，你会怎么做？"
},

{
    "picture":"assets/picture2.jpg",
    "question":"你在巴士上看见老人没有座位。"
},

{
    "picture":"assets/picture3.jpg",
    "question":"学校举办义卖会。"
},

{
    "picture":"assets/picture4.jpg",
    "question":"你和朋友发生误会。"
}

]

def get_topic():
    return random.choice(ORAL_TOPICS)
