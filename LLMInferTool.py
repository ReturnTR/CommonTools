# 加载模型

from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, LlamaForCausalLM
from transformers.generation import GenerationConfig
import torch
from tqdm import tqdm
from CommonTools.JsonTool import *

ziya_model_path="/home/sankuai/dolphinfs_liuziyun04/LLaMA-Efficient-Tuning-Ziya/ziyav_13B_v1.1"
chatglm2_model_path="/home/sankuai/dolphinfs_liuziyun04/main/chatglm6b2"
chatglm_model_path="/home/sankuai/data/chatGLM-6b"
Qwen_model_path="/home/sankuai/dolphinfs_liuziyun04/DataProcess/Qwen-7B-Chat"

class ZiyaModel():
    
    def __init__(self,model_path=ziya_model_path):
        device = torch.device("cuda")
        self.model = LlamaForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        
    def generate(self,prompt):
        inputs = '<human>:' + prompt.strip() + '\n<bot>:'
        input_ids = self.tokenizer(inputs, return_tensors="pt").input_ids.to(device)
        generate_ids = self.model.generate(
                input_ids,
                max_new_tokens=1024, 
                do_sample = True, 
                top_p = 0.85, 
                temperature = 1.0, 
                repetition_penalty=1., 
                eos_token_id=2, 
                bos_token_id=1, 
                pad_token_id=0)
        output = self.tokenizer.batch_decode(generate_ids)[0]
        return output[len(inputs)+8:-4]

class ChatGLMModel():
    
    def __init__(self,model_path=chatglm2_model_path):
        self.tokenizer = AutoTokenizer.from_pretrained("chatglm6b2", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("chatglm6b2", trust_remote_code=True).half().cuda()
        self.model = self.model.eval()
        
    def generate(self,prompt):
        for response, history in self.model.stream_chat(self.tokenizer, prompt, history=[]):pass
        return history[0][1]
    
    
class QwenModel():
    
    def __init__(self,model_path=Qwen_model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        # use bf16
        # model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True, use_bf16=True).eval()
        # use fp16
        # model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True, use_fp16=True).eval()
        # use fp32
        self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True).eval()
        self.model.generation_config = GenerationConfig.from_pretrained(model_path, trust_remote_code=True) # 可指定不同的生成长度、top_p等相关超参
        
    def generate(self,prompt,history=None):
        response, history = self.model.chat(self.tokenizer, prompt, history=history)
        return response

    
    
def test_json(model,filename,prompt_key="input"):
    """
    注：文件格式:字典列表，prompt需要表明键
    默认保存在目标文件夹下，加_generation
    """
    data=load_json(filename)
    new_data=[]
    for item in tqdm(data):
        response= model.generate(item[prompt_key])
        new_data.append({"prompt":item[prompt_key],"predict":response})
    save_jsonl(new_data,filename[:-5]+"_generated.json")
    
    

