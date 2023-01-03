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
        var inputs = document.querySelectorAll(`#${namediv} input`);
        let save = '';

        inputs.forEach(function(input) {
            if (!input.value){
                contador = true
                if (save == namediv){
                    
                }else{
                save = namediv
                alert(`A categoria ${namediv} não foi totalmente preenchida!`)
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

class Mensal{
    constructor() {
        this.key = false;
    }

    setar(idDIv, value){
        var div = document.getElementById(idDIv)
        div.innerHTML = value
    }
}