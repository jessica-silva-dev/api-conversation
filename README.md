Uma api que tenha 1 endpoint apenas

Esse endpoint recebe mensagem de chat. Por enquando recebe apenas msg de texto:

Payload exemplo:
{
   "identifier": "551299876253",
   "contentType": "text",
   "content": "Minha primeira msg..."
}

vc vai precisa salva essa msg no banco, salva o contato caso não exista

tem que ter forma de relacionar o message com o contato para saber de quem é a mensagem.
faz isso por enquando
pode usar o django se quiser, mas faz em python
Dúvidas ? kaskakskkas
assim que vc terminar eu passo mais etapas
mais uma etapas apenas akskak
no final vc vai entender o pq

models

Contact
   name
   identifier
   created_at
   updated_at

Message
   content
   content_type
   created_at
   updated_at
   contact
   
==========Próxima estapa===========

Lembrar de troca o contact com id no endpoint de mensagem para receber o identifier --> OK

identifier tem que ser unique no banco --> OK

valida se o numero contém digito 9 , se não tiver nono digito vc adiciona! --> OK

só é valido para número brasileiros --> OK


Chega mensagem pelo endpoint de message.

Validar se um contato com aquele identifier já existe no banco, caso não exista, cria-lo. --> OK

Agora com o contato, valide se existe um ticket aberto para aquele contato. Caso não exista, cria-lo. --> OK

+ ou - assim o Model:

Quando um ticket é aberto ele já fica com o status open. --> ok
class TicketModel(models.Models): --> ok
     id, 
     contact,
     status: "Aberto" ou "fechado"
     user: Auth.user # vai ser  o User do django -> Pode ser NULL

class MessageModel(modesl.Model):
   contact -> vc remove --> ok
   ticket -> vc adiciona --> ok


=============== Próxima etapa ===============

Atendentes

Criar um novo app chamado matcher --> OK

buscar do banco quais os tickets que tem que tranferir em x tempo

se o ticket tiver aberto, e se não tiver nenhum agent associado ao ticket

um agent tem que estar associado a um user --> OK

pesquisar sobre como criar jobs agendar tarefas 
usar um while = True, sleep de 5 secunds



