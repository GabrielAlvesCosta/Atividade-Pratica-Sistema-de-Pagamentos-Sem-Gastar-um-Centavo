import pytest
import requests
from src.pagamento import processar_compra 

def test_processar_compra_sucesso(mocker):
    mock_gateway = mocker.patch('src.pagamento.enviar_para_gateway')
    
    mock_gateway.return_value = {
        "status": "aprovado",
        "transacao_id": "PAG-123456"
    }
    
    dados_cartao = {"numero": "4000123456789010", "cvv": "123"}
    resultado = processar_compra(usuario_id=1, dados_cartao=dados_cartao, valor=150.0)
    
    assert resultado == "Sucesso! Transação PAG-123456 confirmada."
    mock_gateway.assert_called_once_with(dados_cartao, 150.0)


def test_processar_compra_recusada_sem_limite(mocker):
    mock_gateway = mocker.patch('src.pagamento.enviar_para_gateway')
    
    mock_gateway.return_value = {
        "status": "recusado",
        "motivo": "Cartão sem limite disponível"
    }
    
    dados_cartao = {"numero": "4000123456789010", "cvv": "123"}
    resultado = processar_compra(usuario_id=1, dados_cartao=dados_cartao, valor=9999.0)
    
    assert resultado == "Pagamento recusado. Motivo: Cartão sem limite disponível."


def test_processar_compra_timeout_na_black_friday(mocker):
    mock_post = mocker.patch('src.pagamento.requests.post')
    
    mock_post.side_effect = requests.exceptions.Timeout()
    
    dados_cartao = {"numero": "4000123456789010", "cvv": "123"}
    resultado = processar_compra(usuario_id=1, dados_cartao=dados_cartao, valor=200.0)
    
    assert resultado == "Tempo de resposta esgotado. Verifique sua fatura antes de tentar de novo."