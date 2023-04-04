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
        this.days = 0;
        this.objects = [];
        this.category = {};
        this.insumos = {};
    }
    create_table(name){
        let insert = document.getElementById('container')
        let tb = document.createElement('table')
        tb.id = name
        insert.appendChild(tb)
        let trHeader = document.createElement('tr')
        let th1 = document.createElement('th')
        th1.innerHTML = name
        let th2 = document.createElement('th')
        th2.innerHTML = 'Carga'
        trHeader.appendChild(th1)
        trHeader.appendChild(th2)
        for(var i=1; i < this.days + 1; i++){
            let th = document.createElement('th')
            th.innerHTML = i
            trHeader.appendChild(th)
        }
        tb.appendChild(trHeader)
        return tb
    }
    categoryCreate(name){
        if (name in this.category){
            return
        }else{

            this.category[name] = this.create_table(name)
        }
    }
    insumosCreate(nameTable, nameInsumo, charge){
        if (nameInsumo in this.insumos){
            return
        }else{
            let tb = this.category[nameTable]
            let tr = document.createElement('tr')
            let tdInsumo = document.createElement('td')
            tdInsumo.innerHTML = nameInsumo
            let tdCharge = document.createElement('td')
            tdCharge.innerHTML = charge
            tr.appendChild(tdInsumo)
            tr.appendChild(tdCharge)

            for(var i=1; i < this.days + 1; i++){
                let td = document.createElement('td')
                td.id = nameInsumo + i
                tr.appendChild(td)
            }

            tb.appendChild(tr)
            this.insumos[nameInsumo] = true
        }
    }
    dateCreate(nameInsumo, charge, date){
        console.log(nameInsumo, charge, date)
        let boxDate = document.getElementById(nameInsumo+date)
        boxDate.innerText = charge
    }
    create(){
        for(var i=0; i < this.objects.length; i++){
            this.categoryCreate(this.objects[i][0])
            this.insumosCreate(this.objects[i][0], this.objects[i][1], this.objects[i][4])
            this.dateCreate(this.objects[i][1], this.objects[i][2], this.objects[i][3])
        }
    }
    register(category, item, charge, date, chargePadrao) {
        this.objects.push([category, item, charge, date, chargePadrao])
    }

    config(days){
        this.days = parseInt(days)
    }

    setar(idDIv, value){
        var div = document.getElementById(idDIv)
        div.innerHTML = value
    }
}

const mensal = new Mensal();