import os

import langchain
from langchain import chains
from langchain.llms import GooglePalm
import prompts


class GCPLLM:
    def __init__(self):
        self.rule_summarizaion_template = prompts.GCP_PROMPT
        self.prompt = langchain.PromptTemplate(
            input_variables=["input"],
            template="""{input}""",
        )
        self.chain = chains.LLMChain(
            llm=GooglePalm(temperature=0.0),
            prompt=self.prompt,
        )

    def run(self, rules_textproto):
        rule_query = self.rule_summarizaion_template.safe_substitute(
            rules=rules_textproto
        )
        return self.chain.predict(input=rule_query)
