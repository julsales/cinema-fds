describe('Comprar ingresso', () => {
    it('Adicionando categoria e filme', () => {
    cy.visit('');
    cy.get('[href="/login/?next=/"]').click()
    cy.get(':nth-child(3) > .form-control').type('adm123')
    cy.get(':nth-child(4) > .form-control').type('admin123')
    cy.get('.btn').click()
    cy.get('[href="/pagina_adm/"] > button').should('be.visible')
    cy.get('[href="/pagina_adm/"] > button').click()
    cy.get('[href="/adicionar-genero/"] > button').should('be.visible')
    cy.get('[href="/adicionar-genero/"] > button').click()
    cy.get('#id_category_name').type('categoriateste')
    cy.get('button').click()
    cy.get('[href="/pagina_adm/"] > button').click()
    cy.get('[href="/cadastro-filme/"] > button').should('be.visible')
    cy.get('[href="/cadastro-filme/"] > button').click()
    cy.get('#id_category').select('categoriateste1')
    cy.get('#id_movie_name').type('teste')
    cy.get('#id_price').clear()
    cy.get('#id_price').type('20')
    cy.get('#id_images').type('https://institutofortunato.com.br/wp-content/uploads/2021/05/teste.jpg')
    cy.get('button').click()

    })

    it('Comprando ingressos', () => {
        cy.visit('');
        cy.get('[href="/login/?next=/"]').click()
        cy.get(':nth-child(3) > .form-control').type('123')
        cy.get(':nth-child(4) > .form-control').type('123')
        cy.get('.btn').click()
        cy.get(':nth-child(1) > .card > .card-body > .btn').click()
        cy.get('.swal2-confirm').click()
        cy.get('[href="/cart/"] > button').click()
        cy.get(':nth-child(6) > .btn').click()
        cy.get('[data-seat-id="1-1"]').click({ multiple: true })
        cy.get('[data-seat-id="1-2"]').click({ multiple: true })
        cy.get('.btn').click()
        cy.get('#nome').type('nome')
        cy.get('#btn_pagar').click()
    
            })
    })