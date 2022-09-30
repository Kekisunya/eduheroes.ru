from news.models import *

User = get_user_model()


for i in range(100):
    n = News()
    n.title = 'Новость ' + str(i)
    n. abstract = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis commodo mauris ipsum, ut ultricies lacus tincidunt sed. Sed commodo lacus nec ligula pharetra ullamcorper. Ut nec lorem et mauris commodo varius et ac tellus. Donec ac lacus massa. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas at erat sed nisi aliquam blandit non sed turpis. Vivamus sit amet justo justo. Fusce dignissim, tellus eget lacinia blandit, enim arcu auctor ante, a interdum ipsum enim a elit.'''
    n.content = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis commodo mauris ipsum, ut ultricies lacus tincidunt sed. Sed commodo lacus nec ligula pharetra ullamcorper. Ut nec lorem et mauris commodo varius et ac tellus. Donec ac lacus massa. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas at erat sed nisi aliquam blandit non sed turpis. Vivamus sit amet justo justo. Fusce dignissim, tellus eget lacinia blandit, enim arcu auctor ante, a interdum ipsum enim a elit. Aenean venenatis dapibus quam, a semper nunc tincidunt in. Integer felis risus, blandit ut ultrices nec, sagittis et libero. Integer pulvinar diam purus, id efficitur nibh condimentum at. Mauris dictum augue tortor, scelerisque semper tellus varius ac. Nullam vulputate efficitur nunc, quis commodo neque cursus eget. Donec hendrerit erat pharetra quam volutpat, non scelerisque tortor feugiat.
    
    Cras eleifend ornare sapien et rhoncus. Nam in urna lectus. Sed non rhoncus mauris. Aliquam enim dui, rhoncus ut neque vitae, dignissim rhoncus elit. Curabitur pellentesque turpis non nisi viverra egestas. In id dapibus purus. Donec ut mi nec enim placerat aliquet nec in magna. In hac habitasse platea dictumst. Nulla sed aliquam orci. Curabitur quis neque gravida, dictum massa ac, pharetra orci.
    
    Nam non eros mi. Donec a massa ac eros lacinia pharetra. Aliquam posuere vulputate mauris eget aliquet. Praesent id interdum enim. Pellentesque et elementum magna. Phasellus volutpat a sapien ac porta. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam mauris orci, lobortis vel est a, suscipit tempor libero.
    
    Fusce in purus neque. Quisque a elementum arcu. Nunc porttitor dolor sed eros pulvinar fermentum. Curabitur sit amet sem egestas, posuere libero sed, convallis ex. Nulla elementum felis quis enim imperdiet, in pharetra sapien tincidunt. Vivamus commodo pulvinar nibh eu viverra. Nulla enim eros, luctus vel ante nec, placerat lobortis massa. Etiam quis feugiat libero. Sed ac dapibus sem. Nunc at dolor cursus, congue felis non, posuere dui. Nunc ultricies lacus purus, et blandit nunc dictum pharetra. Nulla justo augue, dapibus eget ipsum ut, convallis cursus justo. Proin nibh augue, lacinia sit amet eleifend vel, ullamcorper nec metus.
    
    Sed luctus blandit massa quis imperdiet. Vivamus id quam pellentesque, lacinia urna quis, semper massa. Phasellus non massa id massa placerat consectetur ut id quam. Integer hendrerit sit amet leo at venenatis. Praesent ornare nunc purus, sit amet dictum nibh pulvinar a. Nam ut pretium mi. Mauris a aliquam nunc, vitae dignissim tellus. Phasellus justo dui, volutpat sit amet risus eget, lacinia rhoncus felis. Pellentesque sit amet neque urna. Proin rhoncus iaculis placerat. Ut dictum lectus bibendum orci tincidunt, non fermentum sapien viverra.
    
    Sed egestas enim et libero convallis varius. Vivamus gravida rutrum nulla, vel faucibus lorem iaculis vitae. Interdum et malesuada fames ac ante ipsum primis in faucibus. In sed consequat felis. Vivamus tincidunt, purus sit amet laoreet vulputate, arcu felis tempor tortor, sit amet facilisis quam felis at augue. Pellentesque lobortis ante sem, aliquam ultrices felis sodales non. Donec a molestie odio. Fusce vel mi vitae velit tincidunt iaculis id nec magna.
    
    In ullamcorper tellus ut purus dapibus sollicitudin. Nunc a nulla ac odio gravida luctus a vitae quam. Suspendisse tellus libero, sollicitudin nec ante vitae, efficitur vulputate turpis. Nullam sit amet lacus nibh. Cras vestibulum bibendum nulla vitae ornare. Proin molestie quam in lacus ornare, eu dapibus urna condimentum. Fusce malesuada velit eu dolor condimentum efficitur. Sed sagittis nisi urna, vitae auctor purus euismod vitae. Etiam sollicitudin, orci a pulvinar volutpat, ex nulla tristique massa, in congue lorem tortor sed est.
    
    Morbi quis placerat diam. Suspendisse potenti. Vivamus bibendum dolor orci, vitae tristique leo dictum at. Etiam tincidunt vehicula purus, nec porta quam interdum a. Nunc lacinia lobortis augue, vel efficitur justo laoreet vitae. Integer vulputate turpis metus, nec faucibus lorem placerat nec. Vestibulum in dolor at arcu euismod pulvinar ut dictum lectus.
    
    Morbi at velit sem. Fusce et ipsum et ante finibus viverra in in velit. Maecenas fermentum odio vitae elit sollicitudin sollicitudin. Aliquam sed ante a mauris placerat lacinia non eu magna. Fusce tincidunt pharetra urna. Vestibulum feugiat, dolor ac mollis tincidunt, nisl odio tempus lacus, nec maximus arcu risus eu purus. Nullam convallis nisl velit, vel mattis dolor posuere non. Maecenas quis augue eget tellus accumsan semper ut nec ligula. Nulla dui justo, tincidunt eget nibh at, accumsan facilisis nulla. Quisque pellentesque ante nulla, eget porttitor ligula semper vel. Nullam scelerisque dictum auctor. Sed rutrum risus ac mi bibendum, nec tempus tortor convallis. Duis laoreet eleifend bibendum.
    
    Donec at nisi eget lorem sagittis rhoncus sit amet sit amet sem. Nam ipsum libero, eleifend eu lectus non, vehicula porta lacus. Donec lacinia quam sed erat porta viverra. Quisque pretium dolor eget ante fermentum malesuada. Fusce nec elit laoreet, pretium mauris at, consequat ligula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean enim massa, tempus eu erat sed, dictum eleifend felis. Cras et ligula vitae nunc aliquet viverra ac eu dui.'''
    n.published = True
    n.save()
    n.categories.add(i%6+1)
    n.authors.add(i%2+1)
    n.published = True
    n.save()

    ['Новости','Бизнес', 'Продажи', 'Методика', 'Взрослые', 'Дети']


['Обучение взрослых',
'Обучение детей',
'ДПО',
'Корпоративное обучение',
'Полная занятость',
'Частичная занятость',
'Удаленка',
'В офисе',]

['Методист',
'Продюсер',
'Куратор',
'Проджект',
'Продакт',]

