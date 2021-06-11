var fr=new FileReader();
            fr.onload=function(){
                'test.json'.textContent=fr.result;
            }
              
console.log(fr.readAsText(files[0]))


save_settings = document.getElementById('save_settings')

custom_scripts       = document.getElementById('custom_scripts')
global_font          = document.getElementById('global_font')
font_size            = document.getElementById('font_size')
inner_radius         = document.getElementById('inner_radius')
outer_radius         = document.getElementById('outer_radius')
pie_tips             = document.getElementById('pie_tips')
restore_original_pos = document.getElementById('restore_original_pos')
trigger_keys         = document.getElementById('trigger_keys')
show_icons           = document.getElementById('show_icons')
maya_rope            = document.getElementById('maya_rope')
blender_slice        = document.getElementById('blender_slice')
latency              = document.getElementById('latency')
held_latency         = document.getElementById('held_latency')
padding              = document.getElementById('padding')
dpi_scale            = document.getElementById('dpi_scale')

console.log(custom_scripts)

let form = document.querySelector('.needs-validation')
console.log(form)

save_settings.addEventListener('click', function (event) {
    if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()
    }
    console.log(123)

    form.classList.add('was-validated')
})