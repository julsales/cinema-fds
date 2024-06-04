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
        cy.get('#id_imagem').attachFile({
            filePath: '8b93a5e2db24a573dd2948709d45c631_pipoca-leite-po-molico-receitas-nestle.jpg',
            encoding: 'base64'
        });
        cy.get('button').click()
        cy.get('[href="/pagina_adm/"] > button').click()
        cy.get('[href="/remover_comida/"] > button').click()
        cy.get('#comida').select(1)
        cy.get('button').click()
        })
})