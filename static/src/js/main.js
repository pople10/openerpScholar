const validateMark = ()=>{
    if($(".markValidation span")!=undefined && 
    $(".markValidation span").html()!=undefined)
        try{
            let mark = parseFloat($(".markValidation span").html());
            console.log(mark)
            if(mark<10.0)
                $(".markValidation span").css("color","red")
            else
                $(".markValidation span").css("color","green")
        }
        catch(e)
        {
            console.log(e)
        }
}
/******************* DOM rendering ****************************/
const condition=()=>{
    if ( $(".oe_secondary_menu_section")!=null&&$(".oe_secondary_menu_section").length!=0)
    {
        let data = document.getElementsByClassName("oe_secondary_menu_section")
        if(data!=null&&data!=undefined&&data.length!=0)
        {
            for(let i=0;i<data.length;i++)
            {
                if(data[i].innerHTML.includes("Professors"))
                {
                    return true;
                }
            }
        }
    }
    return false;
}
const loadedJS = ()=>{
    if (condition())
    {
        setTimeout(()=>{
            clearInterval(interval);
            document.getElementsByClassName('oe_application')[0].children[0].style.display='flex';
            let data = document.getElementsByClassName('oe_secondary_menus_container')[0].getElementsByClassName('oe_secondary_menu');
            let menuElement=[];
            for(let e of data){
                if(e.style.display!='none'){
                    elementActive = e.getElementsByClassName('oe_active')[0].parentNode;
                    let i = 0;
                    let elements = e.getElementsByClassName('oe_secondary_menu_section');
                    let containers = e.getElementsByClassName('oe_secondary_submenu');
                    while(i<elements.length)    
                        menuElement.push({elementclickabe:elements[i],container:containers[i],open:elementActive==containers[i],length:containers[i++].children.length});
                    break;
                }
            }

            
            let heightEle = 33; 
            changeElementActive(false);

                
            const showhideElement = (e)=>{
                let open = (e.container.style.height =='0px');
                let el = e.elementclickabe.style ;
                if(el.background != 'rgb(0, 123, 255)')
                    e.elementclickabe.style.background = open?'#ffffff26':'transparent';
                e.container.style.height=open?(heightEle*e.length+"px"):"0px";
            }

            function changeElementActive (clickElementDone){
                for(let e of menuElement){
                    e.container.style.height='0px';
                    if(e.open==true){
                        e.elementclickabe.style.background="#007bff"
                        e.container.style.height=heightEle*e.length+"px";
                    }
                    if(clickElementDone==false){
                        e.elementclickabe.addEventListener('click',()=>{showhideElement(e)});
                        for(let c of e.container.children){
                            c.onclick =()=>{ 
                                elementActive = c.parentNode;
                                console.log(elementActive);
                                
                                let i =0;
                                while(i<menuElement.length){
                                    menuElement[i].open = menuElement[i].container==elementActive;
                                    menuElement[i].elementclickabe.removeAttribute('style');
                                    i++;
                                }
                                changeElementActive(true);
                            };
                        }
                    }
                    
                }
            }
            
            if($(".oe_logo")!=null&&$(".oe_logo")!=undefined)
            {
                $("a.oe_logo").css("visibility","visible")
                $(".oe_logo img").attr("src","https://ensah.trackiness.com/resources/images/l.png");
            }
                let valCom=$(".openerp .oe_kanban_view.oe_kanban_ungrouped .oe_kanban_column .oe_kanban_record");
                let cond=$(".oe_fold_column.oe_kanban_record");
                if(cond!=null&&cond!=undefined&&cond.length!=0)
                {
                    let valComChild=$(".oe_fold_column.oe_kanban_record .oe_scholar_vignette");
                    if(valComChild!=null&&valComChild!=undefined&&valComChild.length!=0)
                    {
                        $("head").append("<style>.openerp .oe_kanban_view.oe_kanban_ungrouped .oe_kanban_column .oe_kanban_record { width: 50%!important; }</style>");
                    }
                }
        },2000);
    }
}
var interval = setInterval("loadedJS()",100);
/******************* END DOM rendering ****************************/
$(document).ready(()=>{
    $.ajaxSetup({
        beforeSend:()=>{
            
        },
        success: function(data) {
            if((typeof data)=="object"&&data.hasOwnProperty("result"))
            {
                let result = data.result;
                if(result==null||result==undefined)
                {
                    return;
                }
                if(result===0)
                {
                    swal({ title: "Error!", text: "Operation is not completed.", icon: "error" });
                }
                if(result.hasOwnProperty("doneSwal"))
                {
                    swal({ title: "Success!", text: result.doneSwal, icon: "success" });
                }
                if(result.hasOwnProperty("undoneSwal"))
                {
                    swal({ title: "Error!", text: result.undoneSwal, icon: "error" });
                }
                if(result.hasOwnProperty("warningSwal"))
                {
                    let warning = result.warningSwal;
                    swal({ title: warning.title, text: warning.message, icon: "warning" });
                }
                if((typeof result)=="object" && result[0]!=undefined)
                {
                    let datos = result[0];
                    if((typeof datos)=="object"&&datos.hasOwnProperty("videoLink"))
                    {
                        if($("#videoLink")!=undefined)
                        {
                            if(datos.videoLink!=false)
                                $("#videoLink").attr("src",datos.videoLink)
                            else   
                                $("#videoLink").remove();
                        }
                    }
                }
                if($("li.oe_active[data-id]")!=null&&$("li.oe_active[data-id]")!=undefined&&$("li.oe_active[data-id]").length!=0)
                {
                    let map = [];
                    map["studying"]="#009688";
                    map["studying_adjourned"]="#ffcc00";
                    map["graduated"]="#99cc33";
                    map["excluded"]="#cc3300";
                    let val=map[$("li.oe_active[data-id]").attr("data-id")];
                    $("li.oe_active[data-id]")[0].style.background=val
                    $("li.oe_active[data-id] span.arrow span")[0].style.background=val
                }
            }
        },
        error:()=>{
            //swal({ title: "Error!", text: "Something went wrong!", icon: "error" });
        },
        complete:()=>{
            validateMark();
        }
    });
})
