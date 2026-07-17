// Scroll reveal
function revealOnScroll() {
    var elements = document.querySelectorAll('.card, .vantagem-card, .faq-item');
    elements.forEach(function(el) {
        var rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 60) {
            el.classList.add('visible');
        }
    });
}

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', function() {
    setTimeout(revealOnScroll, 100);
});

// Abas de categorias
document.querySelectorAll('.aba').forEach(function(aba) {
    aba.addEventListener('click', function() {
        document.querySelectorAll('.aba').forEach(function(a) { a.classList.remove('ativa'); });
        this.classList.add('ativa');

        var categoria = this.getAttribute('data-categoria');
        document.querySelectorAll('.grade-categoria').forEach(function(g) {
            g.style.display = 'none';
        });
        var grade = document.querySelector('[data-grade="' + categoria + '"]');
        if (grade) {
            grade.style.display = 'grid';
            grade.querySelectorAll('.card').forEach(function(c) {
                c.classList.remove('visible');
                setTimeout(function() { c.classList.add('visible'); }, 50);
            });
        }
    });
});

// FAQ accordion
document.querySelectorAll('.faq-pergunta').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var item = this.parentElement;
        var ativo = item.classList.contains('ativo');

        document.querySelectorAll('.faq-item').forEach(function(faq) {
            faq.classList.remove('ativo');
        });

        if (!ativo) item.classList.add('ativo');
    });
});

// Modal de compra
document.querySelectorAll('.btn-comprar').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var categoria = this.getAttribute('data-categoria');
        var quantidade = this.getAttribute('data-quantidade');
        var preco = this.getAttribute('data-preco');

        document.getElementById('modal-categoria').textContent = categoria;
        document.getElementById('modal-quantidade').textContent = quantidade;
        document.getElementById('modal-preco').textContent = 'R$ ' + preco;

        document.getElementById('form-categoria').value = categoria;
        document.getElementById('form-quantidade').value = quantidade;
        document.getElementById('form-preco').value = preco;

        document.getElementById('modal-compra').classList.add('ativo');
        document.body.style.overflow = 'hidden';
    });
});

document.getElementById('modal-fechar').addEventListener('click', function() {
    document.getElementById('modal-compra').classList.remove('ativo');
    document.body.style.overflow = '';
});

document.getElementById('modal-compra').addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.remove('ativo');
        document.body.style.overflow = '';
    }
});

// Fechar modal com ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        var modal = document.getElementById('modal-compra');
        if (modal.classList.contains('ativo')) {
            modal.classList.remove('ativo');
            document.body.style.overflow = '';
        }
    }
});
