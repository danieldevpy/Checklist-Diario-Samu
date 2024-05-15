class Main{
    constructor() {
        this.key = false;
        this.columns;
        this.pacotes;
      }
    config(){
        this.pacotes = document.querySelectorAll("#pacote")
    }

    check(){

    var pct = document.querySelectorAll("#pacote")
    let contador = false
    pct.forEach(function(thisdiv) {
        var childrens = thisdiv.children[1];
        let namediv = childrens.id
        var nameAttribute = childrens.getAttribute("name");
        console.log(nameAttribute)
        var inputs = document.querySelectorAll(`#${namediv} input`);
        let save = '';

        inputs.forEach(function(input) {
            if (!input.value){
                contador = true
                if (save == namediv){
                    
                }else{
                save = namediv
                alert(`A categoria ${nameAttribute} não foi totalmente preenchida!`)
                }
            }
        });
        });
    if (!contador){
        let form = document.getElementById("form");
        form.submit();
    }else{
        contador = false
    }
    }
    modify_key(){
        if (this.key == false){
             this.key = true;
        }
        else{
             this.key = false;
        }
     }
    add_column(column){
        this.columns.push(column)
    }
    btn_back(){
        if (!this.key){
            this.modify_key();
            this.pacotes.forEach(function(thisdiv) {
                if (thisdiv.style.display == 'none'){
                    thisdiv.style.display = 'flex';
                };
                if (thisdiv.className == 'pacote open'){
                   var childrens = thisdiv.children[1];
                   childrens.className = 'display_closed';
                    thisdiv.className = 'pacote closed'
                };
            });
            setTimeout(() => {
               this.modify_key();
            }, "200"
            )
        }

    }
    clicked(thisdiv){
        if (!this.key){
            this.modify_key();
            if (thisdiv.className == 'pacote closed'){
                if (!this.columns){
                    this.config();
                }
                this.pacotes.forEach(function(divs) {
                    if (thisdiv == divs){
                        divs.className = 'pacote open';
                        var childrens = divs.children[1];
                        childrens.className = 'display_open';
                    }
                    else{
                        divs.className = 'pacote closed';
                        divs.style.display = 'none';
                        var childrens = divs.children[1];
                        childrens.className = 'display_closed';

                    }
            });
            }
            this.modify_key();
    //        if (div.className == 'pacote closed'){
    //            div.className = 'pacote open';
    //        }
    //        if (category.className == 'display_closed'){
    //            category.className = 'display_open';
    //        }
    //    }
    }
    }
}


async function exibirPDF(vtr, mes, fol, ano) {
    let url_atual = window.location.href.split('/')
    console.log(url_atual)
    let url = `${url_atual[0]}//${url_atual[2]}/generate_pdf_r_mensal/${vtr}/${mes}/${fol}/${ano}`
    const pdfContainer = document.getElementById('pdfContainer');

    const loading = document.getElementById("loader");
    const msg = document.getElementById("message");

    loading.style = "display:flex;";

    pdfContainer.innerHTML = "";

    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "blob"; // Define o tipo de resposta como blob (binary large object)

    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) { // A requisição foi concluída
        if (xhr.status === 200) { // O status da resposta é 200 (OK)
        const blob = xhr.response; // Obtém o blob da resposta
        const fileUrl = URL.createObjectURL(blob); // Cria uma URL temporária para o blob

        // Cria um elemento <embed> para exibir o PDF
        const embed = document.createElement("embed");
        embed.src = fileUrl;
        embed.type = "application/pdf";
        embed.style.width = "100%";
        embed.style.height = "100%";

        // Adiciona o elemento <embed> ao container
        pdfContainer.appendChild(embed);
        loading.style.display = "none";
        msg.style.display = "none";
        } else {
            let err = xhr.status;

            switch(err){
                case 404:
                    loading.style = "display:none;"
                    msg.style.display = "flex";
                    msg.childNodes[0].innerText = "Não há registros nessa data escolhida!";
                   
            }
        console.log("Erro na requisição. Status: " + xhr.status);
        }
    }
    };
    xhr.send();
    

}