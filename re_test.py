import re
s = '<iframe frameborder="0" height="200" marginheight="0" marginwidth="0" scrolling="no" thesrc="//feedback.aliexpress.com/display/productEvaluation.htm?productId=32830652654&amp;ownerMemberId=223068979&amp;companyId=232853360&amp;memberType=seller&amp;startValidDate=&amp;i18n=true" width="100%"></iframe>'
ownerMemberId = re.findall(r'ownerMemberId=\d+',s)
print(ownerMemberId)
productId = re.findall(r'productId=\d+',s)
print(productId)