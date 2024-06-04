describe('Adicionar comida', () => {
    it('Adicionando comida', () => {
        cy.visit('');
        cy.get('[href="/login/?next=/"]').click()
        cy.get(':nth-child(3) > .form-control').type('adm123')
        cy.get(':nth-child(4) > .form-control').type('admin123')
        cy.get(':nth-child(5) > .btn').click()
        cy.get('[href="/pagina_adm/"] > button').should('be.visible')
        cy.get('[href="/pagina_adm/"] > button').click()
        cy.get('[href="/adicionar_comida/"] > button').should('be.visible')
        cy.get('[href="/adicionar_comida/"] > button').click()
        cy.get('#id_nome').type('pipoca')
        cy.get('#id_preco').type('10')
    
        })
})