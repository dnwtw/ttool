import ebooklib
from lxml import etree
from ebooklib import epub
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

model = AutoModelForSeq2SeqLM.from_pretrained(r"G:\AIModels\nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained(r"G:\AIModels\nllb-200-distilled-600M")

translator = pipeline(
    device=0,
    task="translation",
    model=model,
    tokenizer=tokenizer,
    src_lang="eng_Latn",
    tgt_lang="zho_Hans",
    max_length=2048,
)

item: epub.EpubHtml

# 打开原始的epub文件
book = epub.read_epub(r"G:\电子书\Rust\rust for rustaceans.epub")

for index, item in enumerate(book.get_items()):
    print(f"开始解析第[{index + 1}]个文档")
    # 以文档为单位解析
    if item.get_type() == ebooklib.ITEM_DOCUMENT:

        tree = etree.HTML(item.get_content())

        # 标题
        h1_list = tree.xpath('//h1')
        for h1 in h1_list:
            h1_text = "".join(h1.xpath(".//text()"))
            print("正在翻译标题")
            h1_text_trans = translator(h1_text)["translation_text"]
            print(f"原文:{h1_text}")
            print(f"译文:{h1_text_trans}")
            print("正在将译文写入文档...")
            translation = etree.Element("h1")
            translation.attrib["style"] = "color: blue;"
            translation.text = f"译文: {h1_text_trans}。"
            h1.addnext(translation)

        # 内容段落
        for p in tree.xpath("//p"):
            p_text = "".join(p.xpath(".//text()"))
            print("正在翻译正文")
            p_text_trans = translator(p_text)["translation_text"]
            print(f"原文:{p_text}")
            print(f"译文:{p_text_trans}")
            print("正在将译文写入文档...")

            translation = etree.Element("p")
            translation.attrib["style"] = "color: blue;"
            translation.text = f"译文: {p_text_trans}。"
            p.addnext(translation)

        # 更新书本的 xhtml 内容
        item.set_content(etree.tostring(tree, pretty_print=True, encoding="unicode"))

# 保存修改后的epub文件
epub.write_epub(r"G:\电子书\Rust\t1.epub", book)
