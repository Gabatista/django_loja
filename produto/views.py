from django.shortcuts import render, redirect, reverse,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from . import models

from pprint import pprint

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 5


class ProdutoDetalhes(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarCarrinho(View):
    def get(self, *args, **kwargs):
        #excluindo carrinho
      #if self.request.session.get('carrinho'):
      #  del self.request.session['carrinho']
      #  self.request.session.save()


        http_referer = self.request.META.get('HTTP_REFERER',reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não encontrado'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promo
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Produto sem estoque'
            )
            return redirect(http_referer)

        #verificando o carrinho e a sessão existem/criando a sessão caso não tenha
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_atual = carrinho[variacao_id]['quantidade']
            quantidade_atual += 1

            if variacao_estoque < quantidade_atual:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente, altere a quantidade do item'
                    f'do produto "{produto.nome}".'
                    f'Há {variacao_estoque} no carrinho'
                )
                quantidade_atual = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_atual
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_atual
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_atual
        else:
            carrinho[variacao_id] = {
                'produto_id' : produto.id,
                'produto_nome' : produto.nome,
                'variacao_nome' : variacao_nome,
                'variacao_id' : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo' : preco_unitario,
                'preco_quantitativo_promocional' : preco_unitario_promocional,
                'quantidade' : 1,
                'slug' : slug,
                'imagem' : imagem,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto.nome} adicionado ao carrinho'
        )
        return redirect(http_referer)



class RemoverCarrinho(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get('HTTP_REFERER',reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
                        return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
                        return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request,
            f'Produto {carrinho["produto_nome"]} {carrinho["variacao_nome"] } removido do carrinho'
        )

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return HttpResponse('RemoverDoCarrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho',{})
        }
        return render(self.request, 'produto/carrinho.html',contexto)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')