
var perimetre = 0;
var long = 0;
var larg = 0;
var surface = 0;
(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  let selectTopbar = select('#topbar')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
        if (selectTopbar) {
          selectTopbar.classList.add('topbar-scrolled')
        }
      } else {
        selectHeader.classList.remove('header-scrolled')
        if (selectTopbar) {
          selectTopbar.classList.remove('topbar-scrolled')
        }
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')

  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function (e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function (e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)


  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {

    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });
  // **************
  $("#epp").on('change', function () {
    let verif_file = $("#fileInput")[0].value;
    if (verif_file) {
      // console.log(verif_file);
      var selectElement = document.getElementById("epp");
      var selectedOption = selectElement.options[selectElement.selectedIndex];
      var selectedValue = selectedOption.value;
      let formData = new FormData();
      var mt = document.getElementById("mt").innerText;
      var mt_name = document.getElementById("mt_name").innerText;
      formData.append('mt', mt);
      formData.append('mt_name', mt_name);
      formData.append('selectedValue', selectedValue);
      $.ajax({
        url: '/change_epaisseur',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(perimetre);
          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = prix_matiere_ht + formattedNumber_decoup;
          let total_prix_matiere = prix_decoup_ttc + prix_matiere_ttc;
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);


          // Change the image source
          //  imageElement.src =  'static/img/upload/current.png';
          //  let myDiv = document.getElementById("accordionExample");
          //  myDiv.style.display = "block";
          // let myDiv2 = document.getElementById("prix_total");
          // myDiv2.style.display = "block";

        },
        error: function () {
          alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
        }
      });
    }

  });

  $(document).ready(function () {
    let dropArea = $("#drop-area");

    dropArea.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
      e.preventDefault();
      e.stopPropagation();
    })
      .on('dragover dragenter', function () {
        dropArea.addClass('dragged');
      })
      .on('dragleave dragend drop', function () {
        dropArea.removeClass('dragged');
      })
      .on('drop', function (e) {
        let files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
      });

    $("#fileInput").on('change', function () {
      let files = this.files;
      handleFiles(files);
    });

    function handleFiles(files) {
      // let x = document.getElementById("div_test");
      // var imagejavascript = document.createElement("svg");
      // var im = document.createElement("img");
      // im.src = "images.png";
      // // imagejavascript.src = "arman.svg";
      // imagejavascript.appendChild(im);
      // x.appendChild(im);

      if (files.length > 0) {
        let file = files[0];
        uploadFile(file);
        // if (file.type === 'dxf') {
        //     uploadFile(file);
        // } else {
        //     alert('Veuillez sélectionner un fichier DXF valide.');
        // }
      }
    }

    function uploadFile(file) {
      let formData = new FormData();
      formData.append('file', file);
      let imageElement = document.getElementsByClassName("img_usinage")[0];
      var selectElement = document.getElementById("epp");
      var selectedOption = selectElement.options[selectElement.selectedIndex];
      var selectedValue = selectedOption.value;

      var selectType = document.getElementById("type_usinage");
      var selectedTypeOption = selectType.options[selectElement.selectedIndex];
      var selectedTypeValue = selectedTypeOption.value;

      var qte = document.getElementById("qte");

      var mt = document.getElementById("mt").innerText;
      var mt_name = document.getElementById("mt_name").innerText;
      formData.append('mt', mt);
      formData.append('mt_name', mt_name);
      formData.append('selectedValue', selectedValue);
      formData.append('selectedTypeValue', selectedTypeValue);
      $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          // console.log(data['clients']);
          let prix_decoup_mtr = data['prix'][0][0];
          let prix_matiere_mtr = data['prix'][0][1];
          // console.log(prix_matiere_mtr);
          larg = data['dimension']['larg'] / 1000;
          long = data['dimension']['long'] / 1000;
          var path_folder = data['path_folder'];

          if (larg && long) {
            surface = (larg * long);
            // console.log(surface);
            perimetre = data['perimetre'];
          }
          // if(larg && long){
          //   surface = 2*(larg+long);
          // } else if(larg && long ==0){
          //   surface = larg;
          // } else if(long && larg == 0){
          //   surface = long;
          // }

          let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
          let formattedNumber_decoup = prix_decoup;
          let prix_decoup_ttc = formattedNumber_decoup * 1.2;
          let prix_matiere_ht = prix_matiere_mtr * surface;
          // console.log(prix_matiere_ht);
          let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
          let total_prix_decoup = prix_matiere_ht + formattedNumber_decoup;
          let total_prix_matiere = prix_decoup_ttc + prix_matiere_ttc;
          // console.log(total_prix_decoup);
          document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
          document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
          document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
          document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);
          document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
          document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);


          // Change the image source
          imageElement.src = path_folder + '/current.png';
          let myDiv = document.getElementById("accordionExample");
          myDiv.style.display = "block";
          // let myDiv2 = document.getElementById("prix_total");
          // myDiv2.style.display = "block";

        },
        error: function () {
          alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
        }
      });
    }
  });

  /**
 * Initiate Pure Counter 
 */


  // **************
  // ****************
if( document.getElementById('dateInput')){
  document.getElementById('dateInput').min = new Date().toISOString().split('T')[0];
}
 
  new PureCounter();

})()
function ouvrir_form_envoi() {
  let myDiv = document.getElementById("envoi_div");
  myDiv.style.display = "block";
}
function fermer_envoi() {
  let myDiv = document.getElementById("envoi_div");
  myDiv.style.display = "none";
}
function envoyer_command() {
  let formData = new FormData();

  var selectEpesseurElement = document.getElementById("epp");
  var selectEpesseuredOption = selectEpesseurElement.options[selectEpesseurElement.selectedIndex];
  var selectedEpesseurValue = selectEpesseuredOption.value;

  var selectClientElement = document.getElementById("cient_select");
  var selectedClientOption = selectClientElement.options[selectClientElement .selectedIndex];
  var selectedClientValue = selectedClientOption.value;

  var name_matiere = document.getElementById("mt").innerHTML;
  var type_matiere = document.getElementById("mt_name").innerHTML;

  var selectType = document.getElementById("type_usinage");
  var selectedTypeOption = selectType.options[selectType.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;

  var prix_matiere = document.getElementById("prix_mat_ttc").innerHTML;
  var prix_limeaire = document.getElementById("frais_decoup_ttc").innerHTML;

  var qte = 1;
  // var mt = document.getElementById("mt").innerText;
  // var mt_name = document.getElementById("mt_name").innerText;
  var name_dxf = "test";
  var date_livraison = document.getElementById("dateInput").value;
  var description = document.getElementById("descriptionInput").value;
  console.log(date_livraison);

  var statut = "en_attente";
  formData.append('client_id', selectedClientValue);
  formData.append('statut', statut);
  formData.append('name_matiere', name_matiere);
  formData.append('type_matiere', type_matiere);

  formData.append('type_usinage', selectedTypeValue);
  formData.append('count', qte);
  formData.append('prix_matiere', prix_matiere);

  formData.append('prix_limeaire', prix_limeaire);
  formData.append('name_dxf', name_dxf);
  formData.append('description', description);
  formData.append('date_fin', date_livraison);
  formData.append('epaisseur_id', selectedEpesseurValue);
   $.ajax({
     url: '/new_command',
     type: 'POST',
     data: formData,
     contentType: false,
     processData: false,
     success: function (msg) {
console.log(msg)

     },
     error: function () {
       alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
     }
   });
}
function confirmation(id){
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_confirmer',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {


      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}
function passe_usinage(id){
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_usiner',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {


      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
    }
  });
}