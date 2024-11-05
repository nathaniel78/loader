from django.core.paginator import Paginator

class Pagination():
  # Descrição: o valor padrão para a paginação
  PAG_QTD = 10

  def pg_default(request, lista, qtd=PAG_QTD):
        """função para paginação

        Args:
            request (pagination): retorna paginação
            lista (string): recebe a lista origem
            qtd (int): recebe o valor de paginação

        Returns:
            pagination: retorna paginação
            Info: para desativar o filtro html uso o |safe
            Url: https://docs.djangoproject.com/en/4.2/topics/pagination/
        """
        page = request.GET.get('page', 1) # type: ignore
        paginator = Paginator(lista, qtd)

        try:
            pg = paginator.page(page)
            return pg
        except PageNotAnInteger: # noqa: F821
            pg = pginator.page(1) # noqa: F821
            return pg
        except EmptyPage: # noqa: F821
            pg = paginator.page(paginator.num_pages)
            return pg