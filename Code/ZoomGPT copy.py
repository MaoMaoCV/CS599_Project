import openai
import re


def chat_with_gpt4(prompt, model="gpt-4-1106-preview", temperature=0.7, max_tokens=150, api_key='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'):
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "Your system message here."},
                      {"role": "user", "content": prompt}],
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

def parse_roles_from_moderator(response):
    roles = []
    pattern = r'([Dr|Mr|Ms].+?), (.+)'  # 正则表达式模式

    matches = re.finditer(pattern, response)
    for match in matches:
        name = match.group(1)  # 提取姓名
        background = match.group(2)  # 提取背景描述
        roles.append((name, background))
    return roles

def gpt_conference(start_prompt, meeting_topic, turns=5):
    current_prompt = start_prompt + "\n\nOverall Topic: " + meeting_topic

    for turn in range(turns):
        # 主持人确定本轮的特定任务和参与角色
        if turn == 0:
            current_prompt += f"\n\nFor round {turn + 1} of our discussion on '{meeting_topic}', "
            current_prompt += "we will focus on the following task: "
            current_prompt += "The following roles will participate in this discussion: (Introduce the name and background of the spokesperson, and the output format is as follows: 1. name, background)"
            current_prompt += "The order of speaking is as follows: (The output format is as follows: [name_1, name_2, name_3, ...], list the names of speakers in order within a pair of square brackets). "
            current_prompt += f"\n\nYou are the host of this meeting, and your speech must include the above content. Of course, you can also add any remarks you think are necessary, and you can add or kick out speakers in each round to better complete the tasks of the meeting."
        else:
            current_prompt += f"\n\nYou are the host of this meeting, the above is all the content of the meeting up to this point, you can summarize it as needed, but your speech must include the following content, and you can add or kick out speakers in each round to better complete the tasks of the meeting."
            current_prompt += f"For round {turn + 1} of our discussion on '{meeting_topic}', "
            current_prompt += "we will focus on the following task: "
            current_prompt += "The following roles will participate in this discussion: (Introduce the name and background of the spokesperson, and the output format is as follows: 1. name, background)"
            current_prompt += "The order of speaking is as follows: (The output format is as follows: [name_1, name_2, name_3, ...], list the names of speakers in order within a pair of square brackets). "

        moderator_response = "\n\nGPT (Moderator):" + chat_with_gpt4(current_prompt)
        print(moderator_response)
        current_prompt += f"\n\n {moderator_response}"
        # # 各个 GPT 实例的回应
        # 使用正则表达式提取所有名字
        names = re.findall(r'\[([^\]]+)\]', moderator_response)
        if names:
            roles = names[0].split(', ')  # 分割得到单独的名字


        for role in roles:
            current_prompt += f"\n\nNow you are {role}, the above is all the content of the meeting up to this point, Please give your speech"
            participant_response = chat_with_gpt4(current_prompt)  # 您的函数来与GPT-4进行对话
            print(f"\n\nGPT ({role}): {participant_response}")
            current_prompt += participant_response

# 使用示例
start_prompt = "This is a conference meeting moderated by an AI."
meeting_topic = "The Future of Artificial Intelligence"
gpt_conference(start_prompt, meeting_topic, turns=3)
