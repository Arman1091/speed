

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
  // let navbarlinks = select('#navbar .scrollto', true)
  // const navbarlinksActive = () => {
  //   let position = window.scrollY + 200
  //   navbarlinks.forEach(navbarlink => {
  //     if (!navbarlink.hash) return
  //     let section = select(navbarlink.hash)
  //     if (!section) return
  //     if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
  //       navbarlink.classList.add('active')
  //     } else {
  //       navbarlink.classList.remove('active')
  //     }
  //   })
  // }
  // window.addEventListener('load', navbarlinksActive)
  // onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  // const scrollto = (el) => {
  //   let header = select('#header')
  //   let offset = header.offsetHeight

  //   let elementPos = select(el).offsetTop
  //   window.scrollTo({
  //     top: elementPos - offset,
  //     behavior: 'smooth'
  //   })
  // }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  // let selectHeader = select('#header')
  // let selectTopbar = select('#topbar')
  // if (selectHeader) {
  //   const headerScrolled = () => {
  //     if (window.scrollY > 100) {
  //       selectHeader.classList.add('header-scrolled')
  //       if (selectTopbar) {
  //         selectTopbar.classList.add('topbar-scrolled')
  //       }
  //     } else {
  //       selectHeader.classList.remove('header-scrolled')
  //       if (selectTopbar) {
  //         selectTopbar.classList.remove('topbar-scrolled')
  //       }
  //     }
  //   }
  //   window.addEventListener('load', headerScrolled)
  //   onscroll(document, headerScrolled)
  // }

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
    const modal = document.getElementById('myModal');
    const img = document.getElementById('img_usinage');
    const modalImg = document.getElementById('modalImage');
    const closeBtn = document.getElementsByClassName('close')[0];
    const zoomInBtn = document.getElementById('zoomIn');
    const zoomOutBtn = document.getElementById('zoomOut');
    let scale = 1;
    let originX = 0;
    let originY = 0;

    img.onclick = function () {
      modal.style.display = 'block';
      modalImg.src = this.src;
      scale = 1;
      modalImg.style.transform = `scale(${scale})`;
      modalImg.style.transformOrigin = `center center`;
    }

    closeBtn.onclick = function () {
      modal.style.display = 'none';
    }

    zoomInBtn.onclick = function () {
      scale += 0.1;
      modalImg.style.transform = `scale(${scale})`;
    }

    zoomOutBtn.onclick = function () {
      if (scale > 0.1) {
        scale -= 0.1;
        modalImg.style.transform = `scale(${scale})`;
      }
    }

    modalImg.onclick = function (event) {
      const rect = modalImg.getBoundingClientRect();
      originX = ((event.clientX - rect.left) / rect.width) * 100;
      originY = ((event.clientY - rect.top) / rect.height) * 100;

      modalImg.style.transformOrigin = `${originX}% ${originY}%`;

      scale += 0.1;
      modalImg.style.transform = `scale(${scale})`;
    }

    // Close the modal when clicking outside of the image
    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = 'none';
      }
    }

    $(".prix_ttc_value").each(function (index, element) {
      let value = parseFloat($(element).text()).toFixed(2);
      $(element).html(value);

    });
    $(".prix_ht_value").each(function (index, element) {
      let value = parseFloat($(element).text()).toFixed(2);
      $(element).html(value);

    });
    $('#dismiss').on('click', function () {
      $('#sidebar').removeClass('active');

    });

    $('#sidebarCollapse').on('click', function () {
      $('#sidebar').addClass('active');

      $('.collapse.in').toggleClass('in');
      $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
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

  if (document.getElementById("errMsg")) {
    clearErrorMsg();
  }


  if (document.getElementsByName('mode_emp')) {
    var radios = document.getElementsByName('mode_emp');
    radios.forEach(function (radio) {
      radio.addEventListener('change', function () {

        let verif_file = document.getElementById("fileInput").value;
        var prix_total_ht = document.getElementById("prix_lin_ht").innerHTML;
        var prix_total_ttc = document.getElementById("prix_lin_ttc").innerHTML;
        if (verif_file) {
          if (this.value == "livraison") {
            var selectDevisProElement = document.getElementById("cients_devis_pro");
            var selectDevisProOption = selectDevisProElement.options[selectDevisProElement.selectedIndex];
            var client_id = selectDevisProOption.value;
            let formData = new FormData();
            formData.append('client_id', client_id);
            $.ajax({
              url: '/get_client_data',
              type: 'POST',
              data: formData,
              contentType: false,
              processData: false,
              success: function (data) {

                var prix_livr_ht = data[0]["prix_livr"];
                document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) + prix_livr_ht).toFixed(2);;
                document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) + 1.2 * prix_livr_ht).toFixed(2);;
                document.getElementById("scructure_livraison_form").style.display = "block";
                document.getElementById("mode_livr_envoi").checked = true;
                document.getElementById('prix_livr').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
                document.getElementById('prix_livr_ht').innerHTML = prix_livr_ht;

              },
              error: function () {
                alert('L\'erreur du  serveur ');
              }
            });



          } else {

            var prix_livr_ht = document.getElementById('prix_livr_ht').innerHTML;
            document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) - prix_livr_ht).toFixed(2);
            document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) - 1.2 * prix_livr_ht).toFixed(2);
            document.getElementById("scructure_livraison_form").style.display = "none";
            document.getElementById("mode_emp_envoi").checked = true;

          }

        } else {
          var text_bn = document.getElementById("text_btn");

          // text_bn.classList.add("active-case");
          if (text_bn.classList.contains("active-case")) {
            if (this.value == "livraison") {
              var selectDevisProElement = document.getElementById("cients_devis_pro");
              var selectDevisProOption = selectDevisProElement.options[selectDevisProElement.selectedIndex];
              var client_id = selectDevisProOption.value;
              let formData = new FormData();
              formData.append('client_id', client_id);
              $.ajax({
                url: '/get_client_data',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function (data) {

                  prix_livr_ht = data[0]["prix_livr"];
                  document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) + parseFloat(prix_livr_ht)).toFixed(2);
                  document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) + 1.2 * prix_livr_ht).toFixed(2);
                  document.getElementById("text_prix_livr_div").style.display = "block";
                  document.getElementById("mode_livr_envoi").checked = true;
                  document.getElementById("addresse_div").style.display = "block";
                  document.getElementById('prix_livr_text').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
                  document.getElementById('prix_livr_text_ht').innerHTML = prix_livr_ht;


                },
                error: function () {
                  alert('L\'erreur du  serveur ');
                }
              });
            } else {
              prix_livr_ht = document.getElementById('prix_livr_text_ht').innerHTML;
              document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) - prix_livr_ht).toFixed(2);
              document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) - 1.2 * prix_livr_ht).toFixed(2);
              document.getElementById("text_prix_livr_div").style.display = "none";
              document.getElementById("mode_emp_envoi").checked = true;
              document.getElementById("addresse_div").style.display = "none";
              document.getElementById('prix_livr_text_ht').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
            }
          }

        }

      });
    });

  }

  if (document.getElementsByName('mode_livr')) {
    var radios = document.getElementsByName('mode_livr');
    radios.forEach(function (radio) {
      radio.addEventListener('change', function () {
        let verif_file = document.getElementById("fileInput").value;
        var prix_total_ht = document.getElementById("prix_lin_ht").innerHTML;
        var prix_total_ttc = document.getElementById("prix_lin_ttc").innerHTML;
        var prix_livr_ht = 0;
        if (verif_file) {

          // prix_livr_ht = document.getElementById("prix_livr_ht").innerHTML;
          if (this.value == "livraison") {
            var selectElement = document.getElementById("client_select");
            var selectOption = selectElement.options[selectElement.selectedIndex];
            var client_id = selectOption.value;
            let formData = new FormData();
            formData.append('client_id', client_id);
            $.ajax({
              url: '/get_client_data',
              type: 'POST',
              data: formData,
              contentType: false,
              processData: false,
              success: function (data) {

                let prix_livr_ht = data[0]["prix_livr"];
                document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) + parseFloat(prix_livr_ht)).toFixed(2);
                document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) + 1.2 * parseFloat(prix_livr_ht)).toFixed(2);;
                document.getElementById("scructure_livraison_form").style.display = "block";
                document.getElementById("addresse_div").style.display = "block";
                document.getElementById("mode_livr").checked = true;
                document.getElementById('prix_livr').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
                document.getElementById('prix_livr_ht').innerHTML = prix_livr_ht;

              },
              error: function () {
                alert('L\'erreur du  serveur ');
              }
            });



          } else {

            var prix_livr_ht = document.getElementById('prix_livr_ht').innerHTML;
            document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) - prix_livr_ht).toFixed(2);
            document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) - 1.2 * prix_livr_ht).toFixed(2);
            document.getElementById("scructure_livraison_form").style.display = "none";
            document.getElementById("mode_emp").checked = true;
            document.getElementById("addresse_div").style.display = "none";

          }
        } else {
          var text_bn = document.getElementById("text_btn");
          if (text_bn.classList.contains("active-case")) {

            if (this.value == "livraison") {
              var selectElement = document.getElementById("client_select");
              var selectOption = selectElement.options[selectElement.selectedIndex];
              var client_id = selectOption.value;
              let formData = new FormData();
              formData.append('client_id', client_id);
              $.ajax({
                url: '/get_client_data',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function (data) {

                  let prix_livr_ht = data[0]["prix_livr"];
                  document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) + prix_livr_ht).toFixed(2);
                  document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) + 1.2 * prix_livr_ht).toFixed(2);
                  document.getElementById("text_prix_livr_div").style.display = "block";
                  // document.getElementById("adresse_envoi_form").reset();
                  document.getElementById("addresse_div").style.display = "block";
                  document.getElementById("mode_livr").checked = true;

                  document.getElementById('prix_livr_text').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
                  document.getElementById('prix_livr_text_ht').innerHTML = prix_livr_ht;

                },
                error: function () {
                  alert('L\'erreur du  serveur ');
                }
              });



            } else {
              let prix_livr_ht = document.getElementById('prix_livr_text_ht').innerHTML;
              document.getElementById("prix_lin_ht").innerHTML = parseFloat(prix_total_ht) - prix_livr_ht;
              document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) - 1.2 * prix_livr_ht).toFixed(2);
              document.getElementById("text_prix_livr_div").style.display = "none";
              document.getElementById("addresse_div").style.display = "none";
              // document.getElementById('adresse_envoi_form').reset();
              document.getElementById("mode_emp").checked = true;
            }
            // document.getElementById("prix_livr_text_ht").innerHTML = prix_livr_ht.toFixed(2);
            // document.getElementById('prix_livr_text').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
          }
        }

      });
    });

  }





  // *********counter******************


  const incrementButton = document.getElementById('increment');
  const decrementButton = document.getElementById('decrement');
  const incrementButtonsPlaque = document.getElementsByClassName("increment_plaque");
  const decrementButtonsPlaque = document.getElementsByClassName("decrement_plaque");

  function incrementCounter() {
    const counterElement = document.getElementById('qte');
    let count = counterElement.value;
    count++;
    counterElement.value = count;
    let verif_file = document.getElementById("fileInput").value;
    if (verif_file) {
      let prix_mat_ht = document.getElementById("prix_mat_ht").innerText;

      let prix_mat_ttc = document.getElementById("prix_mat_ttc").innerText;
      let frais_decoup_ht = document.getElementById("frais_decoup_ht").innerText;
      let frais_decoup_ttc = document.getElementById("frais_decoup_ttc").innerText;
      let qte_percages = parseFloat(document.getElementById("qte_percage").innerText);
      let prix_percages_ht = 0;
      if (qte_percages) {
        prix_percages_ht = qte_percages * 0.3;
      }
      let prix_percages_ttc = 1.2 * prix_percages_ht;
      document.getElementById("prix_lin_ht").innerHTML = (count * (parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht) + prix_percages_ht)).toFixed(2);
      document.getElementById("prix_lin_ttc").innerHTML = (count * (parseFloat(prix_mat_ttc) + parseFloat(frais_decoup_ttc) + prix_percages_ttc)).toFixed(2);
      document.getElementById("qte_structure").innerHTML = count;
    }else if(text_input.value){
      let prix_lettre_ht= document.getElementById("prix_lettre_ht").innerText;
      let prix_lettre_ttc = document.getElementById("prix_lettre_ttc").innerText;
      let nbr_lettres = document.getElementById("nbr_lettres").innerHTML;
      document.getElementById("prix_lin_ht").innerHTML = count * (parseFloat(prix_lettre_ht)* parseFloat(nbr_lettres) );
      document.getElementById("prix_lin_ttc").innerHTML = count * (parseFloat(prix_lettre_ttc) *parseFloat(nbr_lettres));
      document.getElementById("qte_text").innerHTML = count;
    } 
  }


  function decrementCounter() {
    const counterElement = document.getElementById('qte');
    let count = counterElement.value;
    if (count > 1) {
      count--;
      counterElement.value = count;
    }
    let verif_file = document.getElementById("fileInput").value;
    if (verif_file) {
      let prix_mat_ht = document.getElementById("prix_mat_ht").innerText;

      let prix_mat_ttc = document.getElementById("prix_mat_ttc").innerText;
      let frais_decoup_ht = document.getElementById("frais_decoup_ht").innerText;
      let frais_decoup_ttc = document.getElementById("frais_decoup_ttc").innerText;
      let qte_percages = parseFloat(document.getElementById("qte_percage").innerText);
      let prix_percages_ht = 0;
      if (qte_percages) {
        prix_percages_ht = qte_percages * 0.3;
      }
      let prix_percages_ttc = 1.2 * prix_percages_ht;
      document.getElementById("prix_lin_ht").innerHTML = (count * (parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht) + prix_percages_ht)).toFixed(2);;
      document.getElementById("prix_lin_ttc").innerHTML = (count * (parseFloat(prix_mat_ttc) + parseFloat(frais_decoup_ttc) + prix_percages_ttc)).toFixed(2);;
      document.getElementById("qte_structure").innerHTML = count;
    }else if(text_input.value){
      let prix_lettre_ht= document.getElementById("prix_lettre_ht").innerText;
      let prix_lettre_ttc = document.getElementById("prix_lettre_ttc").innerText;
      let nbr_lettres = document.getElementById("nbr_lettres").innerHTML;
      document.getElementById("prix_lin_ht").innerHTML = count * (parseFloat(prix_lettre_ht)* parseFloat(nbr_lettres) );
      document.getElementById("prix_lin_ttc").innerHTML = count * (parseFloat(prix_lettre_ttc) *parseFloat(nbr_lettres));
      document.getElementById("qte_text").innerHTML = count;
    } 
  }


  function incrementPlaque() {
    const counterElement = document.getElementById('qte_plaque');
    let count = counterElement.value;
    count++;
    counterElement.value = count;
  }

  function decrementPlaque() {

    const counterElement = document.getElementById('qte_plaque');
    let count = counterElement.value;
    if (count > 1) {
      count--;
      counterElement.value = count;
    }
  }
  if (incrementButton && decrementButton) {
    incrementButton.addEventListener('click', incrementCounter);
    decrementButton.addEventListener('click', decrementCounter);
  }

  if (incrementButtonsPlaque && decrementButtonsPlaque) {

    for (let i = 0; i < incrementButtonsPlaque.length; i++) {

      let currentElement = incrementButtonsPlaque[i];

      // var elementBefore = currentElement.previousElementSibling;
      // Perform some action on each element (e.g., change its style)
      if (currentElement) {

        currentElement.addEventListener('click', incrementPlaque);
      }
    }
    for (let i = 0; i < decrementButtonsPlaque.length; i++) {
      let currentElement = decrementButtonsPlaque[i];

      // Perform some action on each element (e.g., change its style)
      if (currentElement) {
        currentElement.addEventListener('click', decrementPlaque);
      }
    }

  }


  // ************** changement epaisseur
  $("#epp").on('change', function () {
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;
    var matiereText = selectedMatiereOption.innerText;

    var selectTypeElement = document.getElementById("type_matiere");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectEpaisseurElement = document.getElementById("epp");
    var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
    var selectedEpaisseurValue = selectedEpaisseurOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage");
    let formData = new FormData();
    if (file_btn.classList.contains("active-case")) {
      let verif_file = document.getElementById("fileInput").value;
      if (verif_file) {
        let file = $('#fileInput')[0].files[0];
        console.log(file);
        formData.append('file', file);
      }

      // console.log(verif_file);

      formData.append('matiere_id', selectedMatiereValue);
      formData.append('type_id', selectedTypeValue);
      formData.append('epaisseur_id', selectedEpaisseurValue);
      formData.append('matiereText', matiereText);

      $.ajax({
        url: '/change_epaisseur',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          const length_usg = data["types_usinage"].length;
          console.log("sdsds")
          console.log(length_usg)
          while (selectTypeUsinageElement.options.length > 0) {
            selectTypeUsinageElement.remove(0);
          }
          for (let i = 0; i < length_usg; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["types_usinage"][i].id;
            newOption.text = data["types_usinage"][i].name;
            selectTypeUsinageElement.add(newOption);
          }
          if (data['prix']) {
            var qte = document.getElementById("qte").value;
            let larg = document.getElementById('height_img').innerHTML;
            let long = document.getElementById('width_img').innerHTML;
            let surface = 0;

            if (larg && long) {
              surface = (larg * long);
              // console.log(surface);
            }

            if (matiereText = 'Pmma' && data["types_usinage"][0].name == 'USIL') {

              if (surface < 0.1) {

                var prix_ht_entity = data['prix'][0][0];
              } else if (surface >= 0.1 && surface <= 0.25) {
                var prix_ht_entity = data['prix'][0][1];
              } else {
                var prix_ht_entity = data['prix'][0][2];
              }
              var prix_ht = (qte * prix_ht_entity * surface).toFixed(2);
              var prix_ttc = (1.2 * prix_ht).toFixed(2);
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              document.getElementById("prix_lin_ht").innerHTML = prix_ht;
              document.getElementById("prix_lin_ttc").innerHTML = prix_ttc;
              document.getElementById("qte_structure").innerHTML = qte;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              if (prix_material_div.style.display != 'none' || frais_decoup_div.style.display != 'none') {
                prix_material_div.style.display = 'none'
                frais_decoup_div.style.display = 'none'
              }
            } else {
              var perimetre = document.getElementById('perimetre_totale').innerHTML;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              var qte = document.getElementById("qte").value;
              let prix_decoup_mtr = data['prix'][0][0];
              let prix_matiere_mtr = data['prix'][0][1];
              console.log("perim" + perimetre);
              console.log(prix_decoup_mtr);
              let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
              let formattedNumber_decoup = prix_decoup;
              let prix_decoup_ttc = formattedNumber_decoup * 1.2;
              let prix_matiere_ht = prix_matiere_mtr * surface;

              let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
              let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
              let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
              // console.log(total_prix_decoup);
              document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
              document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
              document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
              document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);

              document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
              document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
              console.log(document.getElementById("prix_mat_ht").innerHTML);
              if (prix_material_div.style.display == 'none' && frais_decoup_div.style.display == 'none') {
                prix_material_div.style.display = 'flex'
                frais_decoup_div.style.display = 'flex'
              }
            }
          }
        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    } else {
      var hauteur = document.getElementById("height");
      var text_input = document.getElementById('text_input');
      var text = text_input.value;
      var textSansEspace = TextWithoutSpaces(text.trim());
      var nbr_lettres = 0;
      if (textSansEspace.length !== 0) {
        nbr_lettres = textSansEspace.length;
        formData.append('nbr_lettres', nbr_lettres);
      }
      formData.append('matiere_id', selectedMatiereValue);
      formData.append('type_id', selectedTypeValue);
      formData.append('epaisseur_id', selectedEpaisseurValue)
      $.ajax({
        url: '/change_lettre_epaisseur',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          console.log(data);

          while (selectTypeUsinageElement.options.length > 0) {
            selectTypeUsinageElement.remove(0);
          }
          const length_usg = data["types_usinage"].length;
          for (let i = 0; i < length_usg; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["types_usinage"][i].id;
            newOption.text = data["types_usinage"][i].name;
            selectTypeUsinageElement.add(newOption);
          }
          while (hauteur.options.length > 0) {
            hauteur.remove(0);
          }
          const length_hauteur = data["hauteurs"].length;
          console.log(length_hauteur);
          for (let i = 0; i < length_hauteur; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["hauteurs"][i].id;
            newOption.text = data["hauteurs"][i].value / 10;
            hauteur.add(newOption);
          }
          if (data['prix']) {
            var qte = document.getElementById("qte").value;
            var prix_rec = data["prix"][0][0];
            var total_prix_ht = nbr_lettres * qte * prix_rec;
            var total_prix_ttc = 1.2 * total_prix_ht;
            document.getElementById('prix_lin_ht').innerHTML = total_prix_ht.toFixed(2);
            document.getElementById('prix_lin_ttc').innerHTML = total_prix_ttc.toFixed(2);
            document.getElementById('prix_lettre_ht').innerHTML = prix_rec.toFixed(2);
            document.getElementById('prix_lettre_ttc').innerHTML = (1.2 * prix_rec).toFixed(2);
            document.getElementById('nbr_lettres').innerHTML = nbr_lettres;
            document.getElementById('qte_text').innerHTML = qte;
          }
        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    }

  })
  $("#height").on('change', function () {

    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;
    var matiereText = selectedMatiereOption.innerText;

    var selectTypeElement = document.getElementById("type_matiere");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectEpaisseurElement = document.getElementById("epp");
    var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
    var selectedEpaisseurValue = selectedEpaisseurOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage");
    var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    var selectedTypeUsinageValue = selectedTypeUsinageOption.value;

    var selectedHauteurElement = document.getElementById("height");
    var selectedHauteurOption = selectedHauteurElement.options[selectedHauteurElement.selectedIndex];
    var selectedHauteurValue = selectedHauteurOption.value;

    var text_input = document.getElementById('text_input');
    var text = text_input.value;
    var textSansEspace = TextWithoutSpaces(text.trim());
    var nbr_lettres = 0;
    if (textSansEspace.length !== 0) {
      nbr_lettres = textSansEspace.length;
    }

    let formData = new FormData();
    formData.append('matiere_id', selectedMatiereValue);
    formData.append('type_id', selectedTypeValue);
    formData.append('epaisseur_id', selectedEpaisseurValue)
    formData.append('type_usinage', selectedTypeUsinageValue);
    formData.append('hauteur', selectedHauteurValue)
    $.ajax({
      url: '/change_lettre_hauteur',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {

        if (data["prix"]) {
          console.log(data["prix"][0]);
          var qte = document.getElementById("qte").value;
          var prix_rec = data["prix"][0];
          var total_prix_ht = nbr_lettres * qte * prix_rec;
          var total_prix_ttc = 1.2 * total_prix_ht;
          document.getElementById('prix_lin_ht').innerHTML = total_prix_ht.toFixed(2);
          document.getElementById('prix_lin_ttc').innerHTML = total_prix_ttc.toFixed(2);
          document.getElementById('prix_lettre_ht').innerHTML = prix_rec.toFixed(2);
          document.getElementById('prix_lettre_ttc').innerHTML = (1.2 * prix_rec).toFixed(2);
          document.getElementById('nbr_lettres').innerHTML = nbr_lettres;
          document.getElementById('qte_text').innerHTML = qte;
        }
      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  })
  //changement type usinage
  $("#type_usinage").on('change', function () {
    let formData = new FormData();
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;
    var matiereText = selectedMatiereOption.innerHTML;

    var selectTypeElement = document.getElementById("type_matiere");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectEpaisseurElement = document.getElementById("epp");
    var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
    var selectedEpaisseurValue = selectedEpaisseurOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage");
    var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    var selectedTypeUsinageValue = selectedTypeUsinageOption.value;
    var selectedUsinageTypeText = selectedTypeUsinageOption.innerHTML;
    if (file_btn.classList.contains("active-case")) {

      let verif_file = document.getElementById("fileInput").value;

      if (verif_file) {
        console.log(matiereText);
        let file = $('#fileInput')[0].files[0];

        formData.append('file', file);

        formData.append('matiere_id', selectedMatiereValue);
        formData.append('type_id', selectedTypeValue);
        formData.append('epaisseur_id', selectedEpaisseurValue);
        formData.append('type_usinage_id', selectedTypeUsinageValue);
        formData.append('matiereText', matiereText);
        formData.append('selectedUsinageTypeText', selectedUsinageTypeText);

        $.ajax({
          url: '/change_type_usinage',
          type: 'POST',
          data: formData,
          contentType: false,
          processData: false,
          success: function (data) {
            var qte = document.getElementById("qte").value;
            let larg = document.getElementById('height_img').innerHTML;
            let long = document.getElementById('width_img').innerHTML;
            let surface = 0;

            if (larg && long) {
              surface = (larg * long);
              // console.log(surface);
            }

            if (matiereText = 'Pmma' && selectedUsinageTypeText == 'USIL') {

              if (surface < 0.1) {
                console.log(data['prix']);
                var prix_ht_entity = data['prix'][0][0];
              } else if (surface >= 0.1 && surface <= 0.25) {
                var prix_ht_entity = data['prix'][0][1];
              } else {
                var prix_ht_entity = data['prix'][0][2];
              }
              console.log("sddsd" + prix_ht_entity);
              var prix_ht = (qte * prix_ht_entity * surface).toFixed(2);
              var prix_ttc = (1.2 * prix_ht).toFixed(2);
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              document.getElementById("prix_lin_ht").innerHTML = prix_ht;
              document.getElementById("prix_lin_ttc").innerHTML = prix_ttc;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              if (prix_material_div.style.display != 'none' || frais_decoup_div.style.display != 'none') {
                prix_material_div.style.display = 'none'
                frais_decoup_div.style.display = 'none'
              }
            } else {
              var perimetre = document.getElementById('perimetre_totale').innerHTML;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              var qte = document.getElementById("qte").value;
              let prix_decoup_mtr = data['prix'][0][0];
              let prix_matiere_mtr = data['prix'][0][1];
              console.log("perim" + perimetre);
              console.log(prix_decoup_mtr);
              let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
              let formattedNumber_decoup = prix_decoup;
              let prix_decoup_ttc = formattedNumber_decoup * 1.2;
              let prix_matiere_ht = prix_matiere_mtr * surface;

              let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
              let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
              let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
              // console.log(total_prix_decoup);
              document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
              document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
              document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
              document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);

              document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
              document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
              console.log(document.getElementById("prix_mat_ht").innerHTML);
              if (prix_material_div.style.display == 'none' && frais_decoup_div.style.display == 'none') {
                prix_material_div.style.display = 'flex'
                frais_decoup_div.style.display = 'flex'
              }
            }

          },
          error: function () {
            alert('Une erreur s\'est produite lors de fare l\'operation.');
          }
        });
      }
    } else {
      var hauteur = document.getElementById("height");
      var text_input = document.getElementById('text_input');
      var text = text_input.value;
      var textSansEspace = TextWithoutSpaces(text.trim());
      var nbr_lettres = 0;
      if (textSansEspace.length !== 0) {
        nbr_lettres = textSansEspace.length;
        formData.append('nbr_lettres', nbr_lettres);
      }
      formData.append('matiere_id', selectedMatiereValue);
      formData.append('type_id', selectedTypeValue);
      formData.append('epaisseur_id', selectedEpaisseurValue)
      formData.append('usinage_id', selectedTypeUsinageValue);
      $.ajax({
        url: '/change_lettre_usinage',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          console.log(data);

          while (hauteur.options.length > 0) {
            hauteur.remove(0);
          }
          const length_hauteur = data["hauteurs"].length;
          console.log(length_hauteur);
          for (let i = 0; i < length_hauteur; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["hauteurs"][i].id;
            newOption.text = data["hauteurs"][i].value / 10;
            hauteur.add(newOption);
          }
          if (data['prix']) {
            var qte = document.getElementById("qte").value;
            var prix_rec = data["prix"][0][0];
            var total_prix_ht = nbr_lettres * qte * prix_rec;
            var total_prix_ttc = 1.2 * total_prix_ht;
            document.getElementById('prix_lin_ht').innerHTML = total_prix_ht.toFixed(2);
            document.getElementById('prix_lin_ttc').innerHTML = total_prix_ttc.toFixed(2);
            document.getElementById('prix_lettre_ht').innerHTML = prix_rec.toFixed(2);
            document.getElementById('prix_lettre_ttc').innerHTML = (1.2 * prix_rec).toFixed(2);
            document.getElementById('nbr_lettres').innerHTML = nbr_lettres;
            document.getElementById('qte_text').innerHTML = qte;
          }
        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    }
  })

  function filterTableRows() {
    var searchText = $('#searche_commande_terminé ').val().toLowerCase();
    console.log(searchText);
    // Iterate through each row in the table body
    $('#historique_table tbody tr').each(function () {
      var currentRow = $(this);
      var tdValues = [];
      currentRow.find('td').each(function () {
        tdValues.push($(this).text());
      });
      var comercials = tdValues[1];
      var clients = tdValues[0];
      // Check if any cell in the row contains the search text

      if (comercials.toLowerCase().indexOf(searchText) === -1 && clients.toLowerCase().indexOf(searchText) === -1) {

        // Hide the row if the search text is not found

        currentRow.hide();

      } else {

        // Show the row if the search text is found

        currentRow.show();

      }
    });
  }

  // Event listener for the input field to trigger filtering on input change
  $('#searche_commande_terminé').keyup(function () {

    filterTableRows();
  });

  function filterTableUsiné() {
    var searchText = $('#search_usiné').val().toLowerCase();
    console.log(searchText);
    // Iterate through each row in the table body
    $('#table_usiné').each(function () {
      var currentRow = $(this);
      var tdValues = [];
      currentRow.find('td').each(function () {
        tdValues.push($(this).text());
      });
      var comercials = tdValues[1];
      var clients = tdValues[0];
      // Check if any cell in the row contains the search text

      if (comercials.toLowerCase().indexOf(searchText) === -1 && clients.toLowerCase().indexOf(searchText) === -1) {

        // Hide the row if the search text is not found

        currentRow.hide();

      } else {

        // Show the row if the search text is found

        currentRow.show();

      }
    });
  }

  // Event listener for the input field to trigger filtering on input change
  $('#search_usiné').keyup(function () {

    filterTableUsiné();
  });

  function filterTableAttents() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('search_en_attants');
    filter = input.value.toLowerCase();
    ul = document.getElementById('en_attents_list');
    li = ul.getElementsByTagName('li');
    var elements = document.querySelectorAll('.contact_name');
    elements.forEach(function (element) {

      let text = element.innerText;
      let current_li = element.closest('li');
      console.log(text.toLowerCase());
      if (text.toLowerCase().indexOf(filter) === -1) {

        // Hide the row if the search text is not found

        current_li.style.display = 'none';

      } else {

        // Show the row if the search text is found

        current_li.style.display = 'block';

      }
    });
    // });
    // var Values = [];
    // for (i = 0; i < li.length; i++) {
    //   Values.push(li[i].innerText);
    //   console.log(Values[i]);
    // txtValue = a.textContent || a.innerText;

    // if (txtValue.toUpperCase().indexOf(filter) > -1) {
    //   li[i].style.display = '';
    // } else {
    //   li[i].style.display = 'none';
    // }
  }


  // Event listener for the input field to trigger filtering on input change
  $('#search_en_attants').keyup(function () {

    filterTableAttents();
  });
  function TextWithoutSpaces(text) {
    return text.replace(/\s/g, '')
  }
  $('#text_input').keyup(function () {
    var selectFontElement = document.getElementById("fontSelect");
    var selectedFontOption = selectFontElement.options[selectFontElement.selectedIndex];
    var selectedFontValue = selectedFontOption.value;
    console.log(selectedFontValue);
    var input = document.getElementById('text_input');
    var text = input.value;
    var testSansEspace = TextWithoutSpaces(text.trim());
    var myTextElement = document.getElementById("text_area");
    myTextElement.style.fontFamily = selectedFontValue; // Replace with your desired font

    // You can also set other font properties like size and color
    myTextElement.style.fontSize = "40px";
    // myTextElement.style.color = "blue";
    myTextElement.innerText = testSansEspace;
    if (testSansEspace.length !== 0) {
      var nbr_lettres = testSansEspace.length;
      let formData = new FormData();
      var selectEppElement = document.getElementById("epp");
      var selectedEppOption = selectEppElement.options[selectEppElement.selectedIndex];
      var selectedEppValue = selectedEppOption.value;

      var selectType = document.getElementById("type_usinage");
      var selectedTypeOption = selectType.options[selectType.selectedIndex];
      var selectedUsinageTypeValue = selectedTypeOption.value;



      var selectMatiereElement = document.getElementById("matiere_select");
      var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
      var mt = selectedMatiereOption.value;


      var selectMatiereTypeElement = document.getElementById("type_matiere");
      var selectedMatiereTypeOption = selectMatiereTypeElement.options[selectMatiereTypeElement.selectedIndex];
      var type = selectedMatiereTypeOption.value;

      var selectHeightElement = document.getElementById("height");
      var selectedHeightOption = selectHeightElement.options[selectHeightElement.selectedIndex];
      var hauteur = selectedHeightOption.value;
      var qte = document.getElementById("qte").value;
      console.log(qte);

      formData.append('mt', mt);
      formData.append('type', type);
      formData.append('type_usinage', selectedUsinageTypeValue);
      formData.append('epaisseur', selectedEppValue);
      formData.append('nbr_lettres ', nbr_lettres);
      formData.append('hauteur', hauteur);
      $.ajax({
        url: '/recevoir_prix_lettre',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          var prix_rec = data["prix"][0][0];
          var total_prix_ht = nbr_lettres * qte * prix_rec;
          var total_prix_ttc = 1.2 * total_prix_ht;
          var text_prix_detailles = document.getElementById('text_prix_detailles');
          var acardion_format_pro = document.getElementById("acardion_format_pro");
          var form_envoyer_usinage_btn = document.getElementById("form_envoyer_usinage_btn");
          var total_prix_detailles = document.getElementById("total_prix_detailles");
          text_prix_detailles.style.display = 'block';
          acardion_format_pro.style.display = 'block';
          form_envoyer_usinage_btn.style.display = 'block';
          total_prix_detailles.style.display = 'flex';
          document.getElementById('prix_lin_ht').innerHTML = total_prix_ht.toFixed(2);
          document.getElementById('prix_lin_ttc').innerHTML = total_prix_ttc.toFixed(2);
          document.getElementById('prix_lettre_ht').innerHTML = prix_rec.toFixed(2);
          document.getElementById('prix_lettre_ttc').innerHTML = (1.2 * prix_rec).toFixed(2);
          document.getElementById('nbr_lettres').innerHTML = nbr_lettres;
          document.getElementById('qte_text').innerHTML = qte;
          document.getElementById("prix_detailles").style.display = "block";
          document.getElementById("text_prix_detailles").style.display = "block";
          document.getElementById("accordionExample").style.display = "none";
        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });

    }


  });
  //   $('#multiple-select').mobiscroll().select({

  //     inputElement: document.getElementById('my-input'),
  //     touchUi: false
  // });
  // **************
  $("#type_matiere").on('change', function () {
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;
    var selectedMatiereText = selectedMatiereOption.innerHTML;

    var selectTypeElement = document.getElementById("type_matiere");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;


    var selectEpaisseurElement = document.getElementById("epp");
    var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
    var selectedEpaisseurValue = selectedEpaisseurOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage");
    let formData = new FormData();
    if (file_btn.classList.contains("active-case")) {
      let verif_file = document.getElementById("fileInput").value;

      if (verif_file) {
        let file = $('#fileInput')[0].files[0];
        console.log(file);
        formData.append('file', file);
      }

      // var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
      // var selectedTypeUsinageValue = selectedTypeUsinageOption.value;

      formData.append('matiere_id', selectedMatiereValue);
      formData.append('type_id', selectedTypeValue);
      formData.append('selectedMatiereText', selectedMatiereText);
      $.ajax({
        url: '/change_type',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          console.log(data["epaisseurs"][0].value)
          while (selectEpaisseurElement.options.length > 0) {
            selectEpaisseurElement.remove(0);
          }
          const length_arr = data["epaisseurs"].length;
          for (let i = 0; i < length_arr; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["epaisseurs"][i].id;
            newOption.text = data["epaisseurs"][i].value;
            selectEpaisseurElement.add(newOption);
          }

          while (selectTypeUsinageElement.options.length > 0) {
            selectTypeUsinageElement.remove(0);
          }
          const length_usg = data["types_usinage"].length;
          console.log(length_usg)
          for (let i = 0; i < length_usg; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["types_usinage"][i].id;
            newOption.text = data["types_usinage"][i].name;
            selectTypeUsinageElement.add(newOption);
          }
          if (data['prix']) {
            var qte = document.getElementById("qte").value;
            let larg = document.getElementById('height_img').innerHTML;
            let long = document.getElementById('width_img').innerHTML;
            let surface = 0;

            if (larg && long) {
              surface = (larg * long);
              // console.log(surface);
            }

            if (selectedMatiereText = 'Pmma' && data['types_usinage'] == 'USIL') {

              if (surface < 0.1) {
                console.log(data['prix']);
                var prix_ht_entity = data['prix'][0][0];
              } else if (surface >= 0.1 && surface <= 0.25) {
                var prix_ht_entity = data['prix'][0][1];
              } else {
                var prix_ht_entity = data['prix'][0][2];
              }
              console.log("sddsd" + prix_ht_entity);
              var prix_ht = (qte * prix_ht_entity * surface).toFixed(2);
              var prix_ttc = (1.2 * prix_ht).toFixed(2);
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              document.getElementById("prix_lin_ht").innerHTML = prix_ht;
              document.getElementById("prix_lin_ttc").innerHTML = prix_ttc;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              if (prix_material_div.style.display != 'none' || frais_decoup_div.style.display != 'none') {
                prix_material_div.style.display = 'none'
                frais_decoup_div.style.display = 'none'
              }
            } else {
              var perimetre = document.getElementById('perimetre_totale').innerHTML;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              var qte = document.getElementById("qte").value;
              let prix_decoup_mtr = data['prix'][0][0];
              let prix_matiere_mtr = data['prix'][0][1];
              console.log("perim" + perimetre);
              console.log(prix_decoup_mtr);
              let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
              let formattedNumber_decoup = prix_decoup;
              let prix_decoup_ttc = formattedNumber_decoup * 1.2;
              let prix_matiere_ht = prix_matiere_mtr * surface;

              let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
              let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup);
              let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc);
              // console.log(total_prix_decoup);
              document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
              document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
              document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
              document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);

              document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
              document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
              console.log(document.getElementById("prix_mat_ht").innerHTML);
              if (prix_material_div.style.display == 'none' && frais_decoup_div.style.display == 'none') {
                prix_material_div.style.display = 'flex'
                frais_decoup_div.style.display = 'flex'
              }
            }

          }

        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    } else {
      var hauteur = document.getElementById("height");
      var text_input = document.getElementById('text_input');
      var text = text_input.value;
      var textSansEspace = TextWithoutSpaces(text.trim());
      var nbr_lettres = 0;
      if (textSansEspace.length !== 0) {
        nbr_lettres = textSansEspace.length;
        formData.append('nbr_lettres', nbr_lettres);
      }
      formData.append('matiere_id', selectedMatiereValue);
      formData.append('type_id', selectedTypeValue);
      $.ajax({
        url: '/change_lettre_type',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          console.log(data);

          while (selectEpaisseurElement.options.length > 0) {
            selectEpaisseurElement.remove(0);
          }


          const length_arr = data["epaisseurs"].length;
          for (let i = 0; i < length_arr; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["epaisseurs"][i].id;
            newOption.text = data["epaisseurs"][i].value;
            selectEpaisseurElement.add(newOption);
          }

          while (selectTypeUsinageElement.options.length > 0) {
            selectTypeUsinageElement.remove(0);
          }
          const length_usg = data["types_usinage"].length;
          for (let i = 0; i < length_usg; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["types_usinage"][i].id;
            newOption.text = data["types_usinage"][i].name;
            selectTypeUsinageElement.add(newOption);
          }
          while (hauteur.options.length > 0) {
            hauteur.remove(0);
          }
          const length_hauteur = data["hauteurs"].length;
          console.log(length_hauteur);
          for (let i = 0; i < length_hauteur; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["hauteurs"][i].id;
            newOption.text = data["hauteurs"][i].value / 10;
            hauteur.add(newOption);
          }
          if (data['prix']) {
            var qte = document.getElementById("qte").value;
            var prix_rec = data["prix"][0][0];
            var total_prix_ht = nbr_lettres * qte * prix_rec;
            var total_prix_ttc = 1.2 * total_prix_ht;
            document.getElementById('prix_lin_ht').innerHTML = total_prix_ht.toFixed(2);
            document.getElementById('prix_lin_ttc').innerHTML = total_prix_ttc.toFixed(2);
            document.getElementById('prix_lettre_ht').innerHTML = prix_rec.toFixed(2);
            document.getElementById('prix_lettre_ttc').innerHTML = (1.2 * prix_rec).toFixed(2);
            document.getElementById('nbr_lettres').innerHTML = nbr_lettres;
            document.getElementById('qte_text').innerHTML = qte;
          }
        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    }


  });
  // changement matiere
  // **************
  $("#matiere_select").on('change', function () {
    var selectMatiereElement = document.getElementById("matiere_select");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;
    var matiereText = selectedMatiereOption.innerText;


    var selectTypeElement = document.getElementById("type_matiere");
    var selectTypeUsinageElement = document.getElementById("type_usinage");
    let formData = new FormData();
    var selectEpaisseurElement = document.getElementById("epp");
    if (file_btn.classList.contains("active-case")) {
      let verif_file = document.getElementById("fileInput").value;
      if (verif_file) {
        let file = $('#fileInput')[0].files[0];
        formData.append('file', file);
      }

      formData.append('matiere_id', selectedMatiereValue);
      formData.append('matiereText', matiereText);
      // formData.append('type_id', selectedTypeValue);


      $.ajax({
        url: '/change_matiere',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {

          while (selectTypeElement.options.length > 0) {
            selectTypeElement.remove(0);
          }
          const length_matieres_types = data["matieres_types"].length;

          for (let i = 0; i < length_matieres_types; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["matieres_types"][i].id;
            newOption.text = data["matieres_types"][i].name;
            selectTypeElement.add(newOption);
          }
          while (selectEpaisseurElement.options.length > 0) {
            selectEpaisseurElement.remove(0);
          }


          const length_arr = data["epaisseurs"].length;
          for (let i = 0; i < length_arr; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["epaisseurs"][i].id;
            newOption.text = data["epaisseurs"][i].value;
            selectEpaisseurElement.add(newOption);
          }

          while (selectTypeUsinageElement.options.length > 0) {
            selectTypeUsinageElement.remove(0);
          }
          const length_usg = data["types_usinage"].length;
          for (let i = 0; i < length_usg; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["types_usinage"][i].id;
            newOption.text = data["types_usinage"][i].name;
            selectTypeUsinageElement.add(newOption);
          }
          var nbr_percage = parseInt(document.getElementById("qte_percage").innerHTML);

          if (data['prix']) {

            let larg = document.getElementById('height_img').innerHTML;
            let long = document.getElementById('width_img').innerHTML;
            let surface = 0;

            if (larg && long) {
              surface = (larg * long);
              // console.log(surface);
            }
            var selects = document.getElementsByClassName('select_plaque_div');
            for (var i = 0; i < selects.length; i++) {
              selects[i].remove();
            }
            if (matiereText === "Newbond") {
              document.getElementById("section_surface_usinage").style.display = "block";
            } else {
              document.getElementById("section_surface_usinage").style.display = "none";
            }
            if (matiereText == 'Pmma' && data["types_usinage"][0].name == 'USIL') {

              if (surface < 0.1) {

                var prix_ht_entity = data['prix'][0][0];
              } else if (surface >= 0.1 && surface <= 0.25) {
                var prix_ht_entity = data['prix'][0][1];
              } else {
                var prix_ht_entity = data['prix'][0][2];
              }
              var prix_ht = (qte * prix_ht_entity * surface).toFixed(2);
              var prix_ttc = (1.2 * prix_ht).toFixed(2);
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              document.getElementById("prix_lin_ht").innerHTML = prix_ht;
              document.getElementById("prix_lin_ttc").innerHTML = prix_ttc;
              document.getElementById("qte_structure").innerHTML = qte;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              if (prix_material_div.style.display != 'none' || frais_decoup_div.style.display != 'none') {
                prix_material_div.style.display = 'none'
                frais_decoup_div.style.display = 'none'
              }
            } else {
              var perimetre = document.getElementById('perimetre_totale').innerHTML;
              var prix_material_div = document.getElementById("prix_material_div");
              var frais_decoup_div = document.getElementById("frais_decoup_div");
              var qte = document.getElementById("qte").value;
              console.log(data['prix'][0]);
              let prix_decoup_mtr = data['prix'][0][0];
              let prix_matiere_mtr = data['prix'][0][1];
              console.log("perim" + perimetre);
              console.log(prix_decoup_mtr);
              let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;
              let formattedNumber_decoup = prix_decoup;
              let prix_decoup_ttc = formattedNumber_decoup * 1.2;
              let prix_matiere_ht = prix_matiere_mtr * surface;

              let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
              let total_prix_decoup = qte * (prix_matiere_ht + formattedNumber_decoup + 0.3 * nbr_percage);
              let total_prix_matiere = qte * (prix_decoup_ttc + prix_matiere_ttc + 0.36 * nbr_percage);
              // console.log(total_prix_decoup);
              if (matiereText === "Newbond") {
                document.getElementById("prix_matiere_hidden").innerHTML = prix_matiere_mtr;
                console.log("zz");
                console.log(prix_matiere_mtr);
              }
              document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
              document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
              document.getElementById("prix_lin_ht").innerHTML = total_prix_decoup.toFixed(2);
              document.getElementById("prix_lin_ttc").innerHTML = total_prix_matiere.toFixed(2);

              document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
              document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
              console.log(document.getElementById("prix_mat_ht").innerHTML);
              if (prix_material_div.style.display == 'none' && frais_decoup_div.style.display == 'none') {
                prix_material_div.style.display = 'flex'
                frais_decoup_div.style.display = 'flex'
              }
            }



          }

        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    } else {
      var hauteur = document.getElementById("height");
      var text_input = document.getElementById('text_input');
      var text = text_input.value;
      var textSansEspace = TextWithoutSpaces(text.trim());
      var nbr_lettres = 0;
      if (textSansEspace.length !== 0) {
        nbr_lettres = textSansEspace.length;
        formData.append('nbr_lettres', nbr_lettres);
      }
      formData.append('matiere_id', selectedMatiereValue);
      $.ajax({
        url: '/change_lettre_matiere',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          console.log(data);
          while (selectTypeElement.options.length > 0) {
            selectTypeElement.remove(0);
          }
          const length_matieres_types = data["matieres_types"].length;

          for (let i = 0; i < length_matieres_types; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["matieres_types"][i].id;
            newOption.text = data["matieres_types"][i].name;
            selectTypeElement.add(newOption);
          }
          while (selectEpaisseurElement.options.length > 0) {
            selectEpaisseurElement.remove(0);
          }


          const length_arr = data["epaisseurs"].length;
          for (let i = 0; i < length_arr; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["epaisseurs"][i].id;
            newOption.text = data["epaisseurs"][i].value;
            selectEpaisseurElement.add(newOption);
          }

          while (selectTypeUsinageElement.options.length > 0) {
            selectTypeUsinageElement.remove(0);
          }
          const length_usg = data["types_usinage"].length;
          for (let i = 0; i < length_usg; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["types_usinage"][i].id;
            newOption.text = data["types_usinage"][i].name;
            selectTypeUsinageElement.add(newOption);
          }
          while (hauteur.options.length > 0) {
            hauteur.remove(0);
          }
          const length_hauteur = data["hauteurs"].length;
          console.log(length_hauteur);
          for (let i = 0; i < length_hauteur; i++) {
            const newOption = document.createElement('option');
            newOption.value = data["hauteurs"][i].id;
            newOption.text = data["hauteurs"][i].value / 10;
            hauteur.add(newOption);
          }
          if (data['prix']) {
            var qte = document.getElementById("qte").value;
            var prix_rec = data["prix"][0][0];
            var total_prix_ht = nbr_lettres * qte * prix_rec;
            var total_prix_ttc = 1.2 * total_prix_ht;
            document.getElementById('prix_lin_ht').innerHTML = total_prix_ht.toFixed(2);
            document.getElementById('prix_lin_ttc').innerHTML = total_prix_ttc.toFixed(2);
            document.getElementById('prix_lettre_ht').innerHTML = prix_rec.toFixed(2);
            document.getElementById('prix_lettre_ttc').innerHTML = (1.2 * prix_rec).toFixed(2);
            document.getElementById('nbr_lettres').innerHTML = nbr_lettres;
            document.getElementById('qte_text').innerHTML = qte;
          }
        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    }




  });
  //changer le role
  $("#role_users").on('change', function () {

    let formData = new FormData();
    var selectRoleElement = document.getElementById("role_users");
    var selectedRoleOption = selectRoleElement.options[selectRoleElement.selectedIndex];
    var selectedRoleValue = selectedRoleOption.value;



    formData.append('role_value', selectedRoleValue);
    console.log(selectedRoleValue);




    $.ajax({
      url: '/users_by_role_selected',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data);
        var table = document.getElementById("users_table");
        var rowCount = table.rows.length;

        // Start from the last row and remove each one
        for (var i = rowCount - 1; i > 0; i--) {
          table.deleteRow(i);
        }
        var nbr = 1;
        for (var i = 0; i < data['users_by_role'].length; i++) {
          let current_user_id = data['users_by_role'][i]['id'];
          var row = table.insertRow();
          var cell0 = row.insertCell(0);
          var cell1 = row.insertCell();
          var cell2 = row.insertCell();
          var cell3 = row.insertCell();
          var cell4 = row.insertCell();
          var cell5 = row.insertCell();
          cell0.innerHTML = nbr++;
          cell1.innerHTML = data['users_by_role'][i]['username'];
          cell2.innerHTML = data['users_by_role'][i]['email'];
          cell3.innerHTML = `+33<span class="user_pure_tel">` + data['users_by_role'][i]['tel'] + `</span>`;
          cell4.innerHTML = "************";

          cell5.innerHTML = `
            <i class="bi bi-pencil-square getInfoBtn" style="font-size: 20px;" ></i>
                      <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;" onclick="delete_selected_user(this,`+ current_user_id + `)"></i>
            `;


        };
      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });

  });

  //changer la matiere de la liste
  $("#matiere_list").on('change', function () {
    var current_user_role = document.getElementById("output_user_role").innerHTML;

    let formData = new FormData();
    var selectMatiereElement = document.getElementById("matiere_list");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;


    var selectTypeElement = document.getElementById("type_list");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage_list");
    var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    var selectedTypeUsinageValue = selectedTypeUsinageOption.value;


    formData.append('matiere_id', selectedMatiereValue);
    // formData.append('type_id', selectedTypeValue);




    $.ajax({
      url: '/matieres_liste',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data["types_matieres"]);

        var table = document.getElementById("matieres_table");
        if (table.style.display == "none") {
          table.style.display = "block";
          var matieres_usil_table = document.getElementById("matieres_usil_table");
          matieres_usil_table.style.display = "none";
          console.log(data["data_usil"]);

        }

        while (selectTypeElement.options.length > 0) {
          selectTypeElement.remove(0);
        }
        const length_arr = data["types_matieres"].length;
        for (let i = 0; i < length_arr; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_matieres"][i].id;
          newOption.text = data["types_matieres"][i].name;
          selectTypeElement.add(newOption);
        }


        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usinage = data["types_usinage"].length;
        for (let i = 0; i < length_usinage; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }



        var rowCount = table.rows.length;

        // Start from the last row and remove each one
        for (var i = rowCount - 1; i > 0; i--) {
          table.deleteRow(i);
        }
        console.log(data['liste_data'].length);
        var nbr = 1;
        for (var i = 0; i < data['liste_data'].length; i++) {

          var row = table.insertRow();
          var cell0 = row.insertCell(0);
          var cell1 = row.insertCell(1);
          var cell2 = row.insertCell(2);
          var cell3 = row.insertCell(3);
          var cell4 = row.insertCell(4);
          var cell5 = row.insertCell(5);
          var cell6 = row.insertCell(6);
          if (current_user_role === "admin") {
            var cell7 = row.insertCell(7);
          }


          cell0.innerHTML = nbr++;
          cell1.innerHTML = data["liste_data"][i]["matiere_name"]
          cell2.innerHTML = data["liste_data"][i]["type_name"]
          cell3.innerHTML = data["liste_data"][i]["usinage_name"]
          cell4.innerHTML = data["liste_data"][i]["epaisseur_value"]


          if (current_user_role === "admin") {
            cell5.innerHTML = `<input type="text" value='` + data["liste_data"][i]["prix_matiere"] + `' class="prix_matiere_input"> €`;
            cell6.innerHTML = `<input type="text" value='` + data["liste_data"][i]["prix_limeaire"] + `'class="prix_limeaire_input">€`;

            cell7.innerHTML = `
            <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                onclick="delete_bridge_row(this)"></i>`;
          } else {
            cell5.innerHTML = `<output type="text" >` + data["liste_data"][i]["prix_matiere"] + ` €</output>`;
            cell6.innerHTML = `<output type="text" >` + data["liste_data"][i]["prix_limeaire"] + `€</output>`;
          }


        };

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });

  });
  //changer le type  de la liste
  $("#type_list").on('change', function () {
    var current_user_role = document.getElementById("output_user_role").innerHTML;
    let formData = new FormData();
    var selectMatiereElement = document.getElementById("matiere_list");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;


    var selectTypeElement = document.getElementById("type_list");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage_list");
    var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    var selectedTypeUsinageValue = selectedTypeUsinageOption.value;

    formData.append('matiere_id', selectedMatiereValue);
    formData.append('type_id', selectedTypeValue);




    $.ajax({
      url: '/type_liste',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data["liste_data"]);
        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usinage = data["types_usinage"].length;
        for (let i = 0; i < length_usinage; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }


        var table = document.getElementById("matieres_table");
        if (table.style.display == "none") {
          table.style.display = "block";
          var matieres_usil_table = document.getElementById("matieres_usil_table");
          matieres_usil_table.style.display = "none";
          console.log(data["data_usil"]);

        }
        var rowCount = table.rows.length;

        // Start from the last row and remove each one
        for (var i = rowCount - 1; i > 0; i--) {
          table.deleteRow(i);
        }
        console.log(data['liste_data'].length);
        var nbr = 1;
        for (var i = 0; i < data['liste_data'].length; i++) {

          var row = table.insertRow();
          var cell0 = row.insertCell(0);
          var cell1 = row.insertCell(1);
          var cell2 = row.insertCell(2);
          var cell3 = row.insertCell(3);
          var cell4 = row.insertCell(4);
          var cell5 = row.insertCell(5);
          var cell6 = row.insertCell(6);
          if (current_user_role === "admin") {
            var cell7 = row.insertCell(7);
          }


          cell0.innerHTML = nbr++;
          cell1.innerHTML = data["liste_data"][i]["matiere_name"]
          cell2.innerHTML = data["liste_data"][i]["type_name"]
          cell3.innerHTML = data["liste_data"][i]["usinage_name"]
          cell4.innerHTML = data["liste_data"][i]["epaisseur_value"]
          if (current_user_role === "admin") {
            cell5.innerHTML = `<input type="text" value='` + data["liste_data"][i]["prix_matiere"] + `' class='prix_matiere_input'> €`;
            cell6.innerHTML = `<input type="text" value='` + data["liste_data"][i]["prix_limeaire"] + `'class='prix_limeaire_input'>€`;
            cell7.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                  onclick="delete_bridge_row(this)"></i>
            `;
          } else {
            cell5.innerHTML = `<output type="text" >` + data["liste_data"][i]["prix_matiere"] + ` €</output>`;
            cell6.innerHTML = `<output type="text" >€ ` + data["liste_data"][i]["prix_limeaire"] + `</output>`;
          }


        };

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });

  });

  $("#type_usinage_list").on('change', function () {
    var current_user_role = document.getElementById("output_user_role").innerHTML; let formData = new FormData();
    var selectMatiereElement = document.getElementById("matiere_list");
    var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
    var selectedMatiereValue = selectedMatiereOption.value;
    var selectedMatiereText = selectedMatiereOption.innerText;


    var selectTypeElement = document.getElementById("type_list");
    var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
    var selectedTypeValue = selectedTypeOption.value;

    var selectTypeUsinageElement = document.getElementById("type_usinage_list");
    var selectedTypeUsinageOption = selectTypeUsinageElement.options[selectTypeUsinageElement.selectedIndex];
    var selectedTypeUsinageValue = selectedTypeUsinageOption.value;

    var selectedTypeUsinageText = selectedTypeUsinageOption.innerText;
    if (selectedTypeUsinageText == "USIL") {
      formData.append('is_usil', true);
    }

    formData.append('matiere_id', selectedMatiereValue);
    formData.append('type_id', selectedTypeValue);
    formData.append('type_usinage_id', selectedTypeUsinageValue);
    formData.append('matiere_name', selectedMatiereText);
    formData.append('usinage_name', selectedTypeUsinageText);




    $.ajax({
      url: '/type_usinage_liste',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        var table2 = document.getElementById("matieres_table");
        if ((data["liste_data"])) {
          ;
          var table = document.getElementById("matieres_table");
          if (table.style.display == "none") {

            table.style.display = "block";
            var matieres_usil_table = document.getElementById("matieres_usil_table");
            matieres_usil_table.style.display = "none";
            console.log(data["data_usil"]);

          }

          var rowCount = table.rows.length;
          // Start from the last row and remove each one
          for (var i = rowCount - 1; i > 0; i--) {
            table.deleteRow(i);
          }
          var nbr = 1;
          for (var i = 0; i < data['liste_data'].length; i++) {

            var row = table.insertRow();
            var cell0 = row.insertCell(0);
            var cell1 = row.insertCell(1);
            var cell2 = row.insertCell(2);
            var cell3 = row.insertCell(3);
            var cell4 = row.insertCell(4);
            var cell5 = row.insertCell(5);
            var cell6 = row.insertCell(6);
            if (current_user_role == "admin") {
              var cell7 = row.insertCell(7);
            }


            cell0.innerHTML = nbr++;
            cell1.innerHTML = data["liste_data"][i]["matiere_name"]
            cell2.innerHTML = data["liste_data"][i]["type_name"]
            cell3.innerHTML = data["liste_data"][i]["usinage_name"]
            cell4.innerHTML = data["liste_data"][i]["epaisseur_value"]
            if (current_user_role == "admin") {
              cell5.innerHTML = `<input type="text" value='` + data["liste_data"][i]["prix_matiere"] + `' class='prix_matiere_input'> €`;
              cell6.innerHTML = `<input type="text" value='` + data["liste_data"][i]["prix_limeaire"] + `'class='prix_limeaire_input'>€`
              cell7.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                      onclick="delete_user('{{user.id}}')"></i>`;
            } else {
              cell5.innerHTML = `<output type="text" >` + data["liste_data"][i]["prix_matiere"] + ` € </output>`;
              cell6.innerHTML = `<output type="text">` + data["liste_data"][i]["prix_limeaire"] + ` €</output>`
            }
          };
        } else {
          if ((data["data_usil"])) {
            var matieres_table = document.getElementById("matieres_table");
            matieres_table.style.display = "none";
            var matieres_usil_table = document.getElementById("matieres_usil_table");
            matieres_usil_table.style.display = "block";
            console.log(data["data_usil"]);

            var rowCount = matieres_usil_table.rows.length;
            // Start from the last row and remove each one
            for (var i = rowCount - 1; i > 0; i--) {
              matieres_usil_table.deleteRow(i);
            }
            console.log(data['data_usil'].length);
            var nbr = 1;
            for (var i = 0; i < data['data_usil'].length; i++) {

              var row = matieres_usil_table.insertRow();
              var cell0 = row.insertCell(0);
              var cell1 = row.insertCell(1);
              var cell2 = row.insertCell(2);
              var cell3 = row.insertCell(3);
              var cell4 = row.insertCell(4);
              var cell5 = row.insertCell(5);
              var cell6 = row.insertCell(6);
              var cell7 = row.insertCell(7);
              if (current_user_role === "admin") {
                var cell8 = row.insertCell(8);
              }

              cell0.innerHTML = nbr++;
              cell1.innerHTML = data["data_usil"][i]["matiere_name"]
              cell2.innerHTML = data["data_usil"][i]["type_name"]
              cell3.innerHTML = data["data_usil"][i]["usinage_name"]
              cell4.innerHTML = data["data_usil"][i]["epaisseur_value"]
              if (current_user_role === "admin") {
                cell5.innerHTML = `<input type="text" value='` + data["data_usil"][i]["prix_1"] + `' class='prix_1_input'> €`;
                cell6.innerHTML = `<input type="text" value='` + data["data_usil"][i]["prix_2"] + `'class='prix_2_input'>€`;
                cell7.innerHTML = `<input type="text" value='` + data["data_usil"][i]["prix_3"] + `'class='prix_3_input'>€`;
                cell8.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                  onclick="delete_bridge_row(this)"></i>`;
              } else {
                cell5.innerHTML = `<output type="text" > ` + data["data_usil"][i]["prix_1"] + ` €</output>`;
                cell6.innerHTML = `<output type="text" >` + data["data_usil"][i]["prix_2"] + ` €</output>`;
                cell7.innerHTML = `<output type="text" >` + data["data_usil"][i]["prix_3"] + ` €</output>`;
              }

            }
          }
        }
      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });

  });
  //change representant
  $("#representant").on('change', function () {
    var current_user_role = document.getElementById("output_user_client_role").innerHTML;


    let formData = new FormData();
    var selectRepresentantElement = document.getElementById("representant");
    var selectedRepresentantOption = selectRepresentantElement.options[selectRepresentantElement.selectedIndex];
    var selectedRepresentantValue = selectedRepresentantOption.value;




    formData.append('representant', selectedRepresentantValue);





    $.ajax({
      url: '/change_representant',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {

        console.log(data["clients"]);
        var table = document.getElementById("clients_table");
        var rowCount = table.rows.length;

        // Start from the last row and remove each one
        for (var i = rowCount - 1; i > 0; i--) {
          table.deleteRow(i);
        }
        var nbr = 1;
        for (var i = 0; i < data['clients'].length; i++) {

          var row = table.insertRow();
          var cell0 = row.insertCell(0);
          var cell1 = row.insertCell();
          var cell2 = row.insertCell();
          var cell3 = row.insertCell();
          var cell4 = row.insertCell();
          var cell5 = row.insertCell();
          var cell6 = row.insertCell();
          var cell7 = row.insertCell();
          var cell8 = row.insertCell();
          cell0.innerHTML = nbr++;
          cell1.innerHTML = data['clients'][i][5];
          cell2.innerHTML = data['clients'][i][0];
          cell3.innerHTML = `<span class="numero_voie_edit_span">` + data['clients'][i][3] + `</span > &nbsp <span class="name_voie_edit_span">` + data['clients'][i][4] + `</span>`;
          cell4.innerHTML = data['clients'][i][2];
          cell5.innerHTML = data['clients'][i][1];
          cell6.innerHTML = data['clients'][i][6];
          cell7.innerHTML = data['clients'][i][7];
          if (current_user_role == "admin") {
            cell8.innerHTML = `
            <output class="rec_client_id" style="visibility: hidden;">`+ data['clients'][i][9] + `</output>
            <output class="rec_user_id" style="visibility: hidden;">`+ data['clients'][i][8] + `</output>
            <i class="bi bi-pencil-square getInfoBtn" style="font-size: 20px;"></i>
            <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;" onclick="delete_user('{{user.id}}')"></i>
          `;
          };
        }


      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });

  });



  $("#cients_devis_pro").on('change', function () {
    var selectDevisProElement = document.getElementById("cients_devis_pro");
    var selectDevisProOption = selectDevisProElement.options[selectDevisProElement.selectedIndex];
    var selectedDevisProValue = selectDevisProOption.value;
    var select = document.getElementById("client_select");
    var options = select.options;

    for (var i = 0; i < options.length; i++) {
      if (options[i].value === selectedDevisProValue) {
        options[i].selected = true;
        break;
      }
    }

    if (selectedDevisProValue == -1) {
      document.getElementById("devis_mode_reception_div").style.display = "none";
    } else {
      document.getElementById("devis_mode_reception_div").style.display = "block";
    }

    var radios = document.getElementsByName('mode_emp');
    var radio_value;
    for (var i = 0; i < radios.length; i++) {
      // Check if the radio button is checked
      if (radios[i].checked) {
        // If checked, log its value

        // You can return the value here if needed
        radio_value = radios[i].value;
        break;
      }
    }

    if (radio_value == "livraison") {
      var text_bn = document.getElementById("text_btn");
      var prix_livr_ht;
      // text_bn.classList.add("active-case");
      if (text_bn.classList.contains("active-case")) {
        prix_livr_ht = document.getElementById('prix_livr_text_ht').innerHTML;
        document.getElementById("text_prix_livr_div").style.display = "none";

      } else {
        prix_livr_ht = document.getElementById('prix_livr_ht').innerHTML;
        document.getElementById("scructure_livraison_form").style.display = "none";
      }

      var prix_total_ht = document.getElementById("prix_lin_ht").innerHTML;
      var prix_total_ttc = document.getElementById("prix_lin_ttc").innerHTML;

      document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) - prix_livr_ht).toFixed(2);
      document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) - 1.2 * prix_livr_ht).toFixed(2);
      document.getElementById("mode_emp").checked = true;
      document.getElementById("mode_emp_envoi").checked = true;
    }


  });


  $("#client_select").on('change', function () {
    var selectElement = document.getElementById("client_select");
    var selectOption = selectElement.options[selectElement.selectedIndex];
    var selectedValue = selectOption.value;
    var selectedDevisProValue = document.getElementById("cients_devis_pro");
    var options = selectedDevisProValue.options;

    for (var i = 0; i < options.length; i++) {
      if (options[i].value === selectedValue) {
        options[i].selected = true;
        break;
      }
    }
    var radios = document.getElementsByName('mode_livr');
    var radio_value;
    for (var i = 0; i < radios.length; i++) {
      // Check if the radio button is checked
      if (radios[i].checked) {
        // If checked, log its value

        // You can return the value here if needed
        radio_value = radios[i].value;
        break;
      }
    }

    if (radio_value == "livraison") {
      var prix_livr_ht = document.getElementById('prix_livr_ht').innerHTML;
      var prix_total_ht = document.getElementById("prix_lin_ht").innerHTML;
      var prix_total_ttc = document.getElementById("prix_lin_ttc").innerHTML;

      document.getElementById("prix_lin_ht").innerHTML = (parseFloat(prix_total_ht) - prix_livr_ht).toFixed(2);
      document.getElementById("prix_lin_ttc").innerHTML = (parseFloat(prix_total_ttc) - 1.2 * prix_livr_ht).toFixed(2);
      document.getElementById("mode_emp").checked = true;
      document.getElementById("scructure_livraison_form").style.display = "none";
      document.getElementById("mode_emp_envoi").checked = true;
    }
    remplie_addresse_case();
  });

  // ***********
  $(document).ready(function () {
    // if (document.getElementById("users_table")) {
    //   var table = document.getElementById("users_table");
    //   var rowCount = 1;
    //   for (var i = 0; i < table.rows.length; i++) {
    //     var cell = table.rows[i].insertCell(0);
    //     cell.innerHTML = rowCount++;
    //   }
    // }

    if (document.getElementById("fontSelect")) {
      var fontSelect = document.getElementById("fontSelect");
      var options = fontSelect.getElementsByTagName("option");
      for (var i = 0; i < options.length; i++) {
        //  console.log(options[i]);
        options[i].style.fontFamily = options[i].value;
      }
      $("#fontSelect").change(function () {
        updateSelectedOptions();
      });

      // Update the selected options text
      function updateSelectedOptions() {

        var selectedOptions = $("#fontSelect").val();
        console.log(selectedOptions); // You can use the selectedOptions array as needed
        var input = document.getElementById('text_input');
        var text = input.value;
        if (text.trim().length !== 0) {
          var myTextElement = document.getElementById("text_area");
          myTextElement.style.fontSize = "40px";
          myTextElement.style.fontFamily = selectedOptions
        }

      }
    }



    let dropArea = $("#drop-area");
    let dropAreaBl = $("#drop-area-bl");

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
      if (files.length > 0) {
        let file = files[0];
        if (file.name.toLowerCase().endsWith('.dxf')) {
          uploadFile(file);
        } else {
          let errMsg = document.getElementById("errMsgSimulation");
          errMsg.innerHTML = "Merci de sélectionnez .dxf file";
          errMsg.style.display = "block";
          setTimeout(() => {
            errMsg.innerHTML = "";
            errMsg.style.display = 'none';
          }, 1500);

        }
      }
    }

    dropAreaBl.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
      e.preventDefault();
      e.stopPropagation();
    })
      .on('dragover dragenter', function () {
        dropAdropAreaBl.addClass('dragged');
      })
      .on('dragleave dragend drop', function () {
        dropAreaBl.removeClass('dragged');
      })
      .on('drop', function (e) {
        let files = e.originalEvent.dataTransfer.files;
        // handleFilesBl(files);
      });

    $("#fileInputBl").on('change', function () {
      let files = this.files;
      // handleFilesBl(files);
    });

    function handleFilesBl(files) {

      // let x = document.getElementById("div_test");
      // var imagejavascript = document.createElement("svg");
      // var im = document.createElement("img");
      // im.src = "images.png";
      // // imagejavascript.src = "arman.svg";
      // imagejavascript.appendChild(im);
      // x.appendChild(im);

      if (files.length > 0) {
        let file = files[0];
        uploadFileBl(file);
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
      let imageElement = document.getElementById("img_usinage");
      var selectElement = document.getElementById("epp");
      var selectedOption = selectElement.options[selectElement.selectedIndex];
      var selectedValue = selectedOption.value;

      var selectType = document.getElementById("type_usinage");
      var selectedTypeOption = selectType.options[selectType.selectedIndex];
      var selectedTypeValue = selectedTypeOption.value;
      var usinage_text = selectedTypeOption.innerHTML;


      var selectMatiereElement = document.getElementById("matiere_select");
      var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
      var mt = selectedMatiereOption.value;
      var mt_text = selectedMatiereOption.innerHTML;

      var selectMatiereTypeElement = document.getElementById("type_matiere");
      var selectedMatiereTypeOption = selectMatiereTypeElement.options[selectMatiereTypeElement.selectedIndex];
      var mt_name = selectedMatiereTypeOption.value;

      var qte = document.getElementById("qte").value;


      // var mt = document.getElementById("mt").innerText;
      // var mt_name = document.getElementById("mt_name").innerText;
      formData.append('mt', mt);
      formData.append('mt_name', mt_name);
      formData.append('selectedValue', selectedValue);
      formData.append('selectedTypeValue', selectedTypeValue);
      formData.append('mt_text', mt_text);
      formData.append('usinage_text', usinage_text);

      if (isAnyFormDataEmpty(formData)) {
        var err_simulation = document.getElementById("err_simulation");
        err_simulation.textContent = "Un ou plusieurs champs du formulaire sont vides";
        err_simulation.style.display = "block";
        setTimeout(() => {
          err_simulation.style.display = 'none';
        }, 1500);

      } else {
        // formData.append('qte', qte);
        $.ajax({
          url: '/upload',
          type: 'POST',
          data: formData,
          contentType: false,
          processData: false,
          success: function (data) {
            if (data["msg"]) {
              let errMsg = document.getElementById("errMsgSimulation");
              errMsg.innerHTML = data["msg"];
              errMsg.style.display = "block";
              setTimeout(() => {
                errMsg.innerHTML = "";
                errMsg.style.display = 'none';
              }, 2000);
            } else {
              var nbr_percage = data['nbr_percage'];
              var path_folder = data['path_folder'];
              let long = data['dimension']['larg'] / 1000;
              let larg = data['dimension']['long'] / 1000;
              console.log("chaper");
              console.log(larg);
              console.log(long);

              let surface = 0, perimetre = 0;
              if (larg && long) {
                surface = (larg * long);
              }
              if (data['perimetre']) {
                let prix_decoup_mtr = data['prix'][0][0];
                let prix_matiere_mtr = data['prix'][0][1];
                console.log(prix_matiere_mtr);

                perimetre = data['perimetre'];
                let prix_decoup = (perimetre * prix_decoup_mtr) / 1000;

                let formattedNumber_decoup = prix_decoup;
                let prix_decoup_ttc = formattedNumber_decoup * 1.2;
                let prix_matiere_ht = prix_matiere_mtr * surface;

                let prix_matiere_ttc = 1.2 * prix_matiere_mtr * surface;
                let total_prix_ht = qte * (prix_matiere_ht + formattedNumber_decoup + nbr_percage * 0.3);
                let total_prix_ttc = qte * (prix_decoup_ttc + prix_matiere_ttc + nbr_percage * 0.36);

                document.getElementById("frais_decoup_ht").innerHTML = formattedNumber_decoup.toFixed(2);
                document.getElementById("frais_decoup_ttc").innerHTML = prix_decoup_ttc.toFixed(2);
                document.getElementById("prix_lin_ht").innerHTML = total_prix_ht.toFixed(2);
                document.getElementById("prix_lin_ttc").innerHTML = total_prix_ttc.toFixed(2);
                document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
                document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
                document.getElementById("qte_structure").innerHTML = qte;
                document.getElementById("qte_percage").innerHTML = nbr_percage;
                document.getElementById("prix_percage").innerHTML = (1.2 * 0.3 * nbr_percage).toFixed(2);
                document.getElementById("scructure_livraison_form").style.display = "none";
                document.getElementById("mode_emp").checked = true;
                document.getElementById("height_label").innerHTML = larg.toFixed(2);
                document.getElementById("width_label").innerHTML = long.toFixed(2);
                if (document.getElementById("devis_mode_reception_div").style.display !== "none") {
                  document.getElementById("devis_mode_reception_div").style.display = "none";
                }
                if (mt_text === "Newbond") {
                  document.getElementById("section_surface_usinage").style.display = "block";
                  document.getElementById("prix_matiere_hidden").innerHTML = prix_matiere_mtr;

                }

                let labels = document.getElementsByClassName("label");

                // Iterate through each element and set the display property to "block"
                for (let i = 0; i < labels.length; i++) {
                  labels[i].style.display = "block";
                }
                var selectElement = document.getElementById('cients_devis_pro');
                // Set the value of the select element to -1
                selectElement.value = "-1";

                document.getElementById("perimetre_totale").innerHTML = perimetre;

                var prix_material_div = document.getElementById("prix_material_div");
                var frais_decoup_div = document.getElementById("frais_decoup_div");
                if (prix_material_div.style.display == 'none' && frais_decoup_div.style.display == 'none') {
                  prix_material_div.style.display = 'flex'
                  frais_decoup_div.style.display = 'flex'
                }


              } else {

                surface = surface.toFixed(2);
                if (surface < 0.1) {

                  var prix_ht_entity = data['prix'][0][0];
                } else if (surface >= 0.1 && surface <= 0.25) {
                  var prix_ht_entity = data['prix'][0][1];
                } else {
                  var prix_ht_entity = data['prix'][0][2];
                }
                var prix_ht = (qte * prix_ht_entity).toFixed(2);
                var prix_ttc = (1.2 * prix_ht).toFixed(2);

                document.getElementById("prix_lin_ht").innerHTML = prix_ht;
                document.getElementById("prix_lin_ttc").innerHTML = prix_ttc;
                document.getElementById("qte_structure").innerHTML = qte;
                var prix_material_div = document.getElementById("prix_material_div");
                var frais_decoup_div = document.getElementById("frais_decoup_div");
                if (prix_material_div.style.display != 'none' || frais_decoup_div.style.display != 'none') {
                  prix_material_div.style.display = 'none'
                  frais_decoup_div.style.display = 'none'
                }


              }
              // Change the image source

              let timestamp = new Date().getTime();
              imageElement.src = `${path_folder}/current.png?${timestamp}`;
              let myDiv = document.getElementById("accordionExample");
              myDiv.style.display = "block";
              let devis_pro = document.getElementById("acardion_format_pro");
              devis_pro.style.display = "block";
              let form_envoyer_usinage_btn = document.getElementById("form_envoyer_usinage_btn");
              if (form_envoyer_usinage_btn) {
                form_envoyer_usinage_btn.style.display = "block";
              }


              let total_prix_detailles = document.getElementById("total_prix_detailles");
              total_prix_detailles.style.display = "flex";
              document.getElementById("height_img").innerHTML = larg.toFixed(2);
              document.getElementById("width_img").innerHTML = long.toFixed(2);
              document.getElementById("prix_detailles").style.display = "block";
              document.getElementById("text_prix_detailles").style.display = "none";
              document.getElementById("surface_usinage").innerHTML = surface.toFixed(2)
              document.getElementById("surface_usinage_hidden").innerHTML = surface.toFixed(2)
            }

          },
          error: function () {
            alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
          }
        });
      }

    }
  });





  /**
 * Initiate Pure Counter
 */
  $("#qte").on('input', function () {
    let qte = this.value;

    if (qte < 0) {

      this.value = 1;
    }
    document.getElementById("qte_structure").innerHTML = qte;
    let verif_file = document.getElementById("fileInput").value;
    let text_input = document.getElementById("text_input");
    if (verif_file) {
      let prix_mat_ht = document.getElementById("prix_mat_ht").innerText;

      let prix_mat_ttc = document.getElementById("prix_mat_ttc").innerText;
      let frais_decoup_ht = document.getElementById("frais_decoup_ht").innerText;
      let frais_decoup_ttc = document.getElementById("frais_decoup_ttc").innerText;
      let qte_percages = parseFloat(document.getElementById("qte_percage").innerText);
      let prix_percages_ht = 0;
      if (qte_percages) {
        prix_percages_ht = qte_percages * 0.3;
      }
      let prix_percages_ttc = 1.2 * prix_percages_ht;
      document.getElementById("prix_lin_ht").innerHTML = qte * (parseFloat(prix_mat_ht) + parseFloat(frais_decoup_ht) + prix_percages_ht);
      document.getElementById("prix_lin_ttc").innerHTML = qte * (parseFloat(prix_mat_ttc) + parseFloat(frais_decoup_ttc) + prix_percages_ttc);

    }else if(text_input.value){
      let prix_lettre_ht= document.getElementById("prix_lettre_ht").innerText;
      let prix_lettre_ttc = document.getElementById("prix_lettre_ttc").innerText;
      let nbr_lettres = document.getElementById("nbr_lettres").innerHTML;
      document.getElementById("prix_lin_ht").innerHTML = qte * (parseFloat(prix_lettre_ht)* parseFloat(nbr_lettres) );
      document.getElementById("prix_lin_ttc").innerHTML = qte * (parseFloat(prix_lettre_ttc) *parseFloat(nbr_lettres));
      document.getElementById("qte_text").innerHTML = qte;
    } 
  });

  // **************
  // ****************
  if (document.getElementById('dateInput')) {
    document.getElementById('dateInput').min = new Date().toISOString().split('T')[0];
  }

  new PureCounter();

})()
function ouvrir_form_envoi() {
  var selectClient = document.getElementById("client_select");
  var selectedClientOption = selectClient.options[selectClient.selectedIndex];
  if (selectedClientOption) {
    document.getElementById("adresse_envoi_form").reset();
    let myDiv = document.getElementById("envoi_div");
    myDiv.style.display = "block";
    myDiv.style.zIndex = "9999";
    document.getElementById("adresse_envoi_form").reset();
    if (document.getElementById("mode_livr").checked == true) {
      document.getElementById("addresse_div").style.display = "block";


    }
    remplie_data();

  } else {
    var msg = document.getElementById("msg_simulation");
    msg.style.display = "block";
    msg.style.color = "orangered"
    msg.textContent = "Vous n'avez pas le client, veuillez ajouter les clients pour pouvoir envoyer la production!";
    setTimeout(function () {
      msg.style.display = "none";
      msg.style.color = "green"
    }, 2000);
  }

  // console.log(document.getElementById('simulation_infos'));
  // document.getElementById('simulation_infos').classList.add('disabled');
  // document.getElementById('simulation_infos').style.zIndex = '-1';


}

function remplie_data() {
  var selectElement = document.getElementById("client_select");
  var selectOption = selectElement.options[selectElement.selectedIndex];
  var selectedValue = selectOption.value;

  let formData = new FormData();
  formData.append('client_id', selectedValue);
  $.ajax({
    url: '/get_client_data',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      console.log(data[0]["prix_livr"]);
      prix_livr_ht = data[0]["prix_livr"];
      document.getElementById("numero_voie_livr").value = data[0]["numero"];
      document.getElementById("nom_voie_livr").value = data[0]["addresse"];
      document.getElementById("cp_livr").value = data[0]["cp"];
      document.getElementById("ville_livr").value = data[0]["ville"];
      document.getElementById('prix_livr').innerHTML = (1.2 * prix_livr_ht).toFixed(2);
      document.getElementById('prix_livr_ht').innerHTML = prix_livr_ht;
    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}

function remplie_addresse_case() {
  var selectElement = document.getElementById("client_select");
  var selectOption = selectElement.options[selectElement.selectedIndex];
  var selectedValue = selectOption.value;

  let formData = new FormData();
  formData.append('client_id', selectedValue);
  $.ajax({
    url: '/get_client_data',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      document.getElementById("numero_voie_livr").value = data[0]["numero"];
      document.getElementById("nom_voie_livr").value = data[0]["addresse"];
      document.getElementById("cp_livr").value = data[0]["cp"];
      document.getElementById("ville_livr").value = data[0]["ville"];
      // document.getElementById('prix_livr').innerHTML = (1.2*prix_livr_ht).toFixed(2);
      // document.getElementById('prix_livr_ht').innerHTML = prix_livr_ht;
      // document.getElementById("mode_emp").checked = true;
    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}
function fermer_envoi() {
  let myDiv = document.getElementById("envoi_div");
  myDiv.style.display = "none";
  document.getElementById("adresse_envoi_form").reset();
  document.getElementById('simulation_infos').style.zIndex = '1';
}
function envoyer_command() {
  let formData = new FormData();

  var selectEpesseurElement = document.getElementById("epp");
  var selectEpesseuredOption = selectEpesseurElement.options[selectEpesseurElement.selectedIndex];
  var selectedEpesseurValue = selectEpesseuredOption.value;

  var selectClientElement = document.getElementById("client_select");

  var selectedClientOption = selectClientElement.options[selectClientElement.selectedIndex];
  var selectedClientValue = selectedClientOption.value;

  var selectMatiereElement = document.getElementById("matiere_select");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var name_matiere = selectedMatiereOption.innerHTML;

  var selectTypeElement = document.getElementById("type_matiere");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var type_matiere = selectedTypeOption.innerText;


  var selectType = document.getElementById("type_usinage");
  var selectedTypeOption = selectType.options[selectType.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;
  var qte = document.getElementById("qte").value;
  var statut = "en_attente";

  var date_livraison = document.getElementById("dateInput").value;
  var description = document.getElementById("descriptionInput").value;

  const selectedRadio = document.querySelector('input[name="mode_livr"]:checked');

  const selectedValue = selectedRadio.value;
  let is_livr = false;
  let numero_voie_livr = document.getElementById("numero_voie_livr").value;
  let nom_voie_livr = document.getElementById("nom_voie_livr").value;
  let cp_livr = document.getElementById("cp_livr").value;
  let ville_livr = document.getElementById("ville_livr").value;
  if (selectedValue == "livraison") {
    formData.append('numero_voie_livr', numero_voie_livr);
    formData.append('nom_voie_livr', nom_voie_livr);
    formData.append('cp_livr', cp_livr);
    formData.append('ville_livr', ville_livr);
  }
  if (!date_livraison) {
    let msg = document.getElementById("msg_div_ouvert");
    let dateInput = document.getElementById("dateInput");
    msg.style.display = "block";
    msg.style.color = "red";
    dateInput.style.border = '1px solid red';
    msg.textContent = " veuillez ajouter la date la production souhaité";
    setTimeout(function () {
      msg.style.display = "none";
      msg.style.color = "green";
      dateInput.style.border = '0';
    }, 2000);
  } else if (selectedValue == "livraison" && (!numero_voie_livr || !nom_voie_livr || !cp_livr || !ville_livr)) {
    let msg = document.getElementById("msg_div_ouvert");
    msg.style.display = "block";
    msg.style.color = "red";
    msg.textContent = " Veuillez remplir tous les champs obligatoires";
    setTimeout(function () {
      msg.style.display = "none";
      msg.style.color = "green";
    }, 2000);
  } else {
    var file_btn = document.getElementById("file_btn");
    var text_bn = document.getElementById("text_btn");
    var prix_ht = document.getElementById("prix_lin_ht").innerHTML;
    formData.append('prix_ht', prix_ht);
    if (file_btn.classList.contains("active-case")) {

      if (selectedValue == "livraison") {
        prix_livr_ht = document.getElementById("prix_livr_ht").innerHTML;
        formData.append('prix_livr_ht', prix_livr_ht);
      }
      let file = $('#fileInput')[0].files[0];
      formData.append('file', file);
      if (name_matiere === "Newbond") {
        var selects = document.querySelectorAll('#plaque_div select');
        var selectedValues = [];
        var selectedQte = [];
        var input = "";
        let i = 0;
        var qte = parseFloat(document.getElementById("qte").value);
        selects.forEach(function (select) {

          let text = select.selectedOptions[0].text;
          selectedValues[i] = text;
          input = select.nextElementSibling;
          selectedQte[i] = input.querySelector('input.qte_plaque').value;
          i++;
        });
        if (selectedValues.length) {
          formData.append('plaques', selectedValues);
          formData.append('qte_plaques', selectedQte);
        }
      }




    } else if (text_bn.classList.contains("active-case")) {
      if (selectedValue == "livraison") {
        var prix_text_livr_ht = document.getElementById("prix_livr_text_ht").innerHTML;
        formData.append('prix_livr_ht', prix_text_livr_ht);
      }
      var text_input = document.getElementById("text_input").value;
      var selectHeightElement = document.getElementById("height");
      var selectedHeightOption = selectHeightElement.options[selectHeightElement.selectedIndex];
      var height = selectedHeightOption.innerHTML;
      var selectFontElement = document.getElementById("fontSelect");
      var selectedFontOption = selectFontElement.options[selectFontElement.selectedIndex];
      var selectedFontValue = selectedFontOption.value;
      var selectedFontText = selectedFontOption.innerText;

      formData.append('height', height);
      formData.append('text_input', text_input);
      formData.append('name_police', selectedFontText);


    }

    // prix_livraison_ttc = document.getElementById("prix_livr_text").innerHTML;
    // prix_livraison_ht = (prix_livraison_ttc/1.2).toFixed(2);
    formData.append('client_id', selectedClientValue);
    formData.append('statut', statut);
    formData.append('name_matiere', name_matiere);
    formData.append('type_matiere', type_matiere);

    formData.append('type_usinage', selectedTypeValue);
    formData.append('count', qte);


    formData.append('description', description);
    formData.append('date_fin', date_livraison);
    formData.append('epaisseur_id', selectedEpesseurValue);
    formData.append('is_livr', is_livr);

    $.ajax({
      url: '/new_command',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {

        let myDiv = document.getElementById("envoi_div");
        myDiv.style.display = "none";

        var msg_simulation = document.getElementById("msg_simulation");
        msg_simulation.textContent = msg;
        msg_simulation.style.display = "block";
        setTimeout(function () {
          window.location.href = "/simulation";
        }, 500);
      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }

}
function confirmation(id) {
  let formData = new FormData();
  let file = $('#fileInputBl')[0].files[0];
  formData.append("file", file);
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_confirmer',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {

      window.location.href = "/en_attente";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}
function supprimer_attente(id) {
  let text = "Voulez vous supprimer la commande?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append("id", id);
    $.ajax({
      url: '/supprimer_attente',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/en_attente";

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }

}
function supprimer_confirmé(id) {
  let text = "Voulez vous supprimer la commande?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append("id", id);
    $.ajax({
      url: '/supprimer_confirmé',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/confirme";

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }

}
function supprimer_usiné(id) {
  let text = "Voulez vous supprimer la commande?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append("id", id);
    $.ajax({
      url: '/supprimer_usiné',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/usiné";

        // Change the image source
        //  imageElement.src =  'static/img/upload/current.png';
        //  let myDiv = document.getElementById("accordionExample");
        //  myDiv.style.display = "block";
        // let myDiv2 = document.getElementById("prix_total");
        // myDiv2.style.display = "block";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }

}

function passe_usinage(id) {
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
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}
function envoie_livraison(id) {
  let formData = new FormData();
  formData.append("id", id);
  $.ajax({
    url: '/change_statut_livré',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      window.location.href = "/usiné";

      // Change the image source
      //  imageElement.src =  'static/img/upload/current.png';
      //  let myDiv = document.getElementById("accordionExample");
      //  myDiv.style.display = "block";
      // let myDiv2 = document.getElementById("prix_total");
      // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}

function telecharger_pdf(user) {

  var selectDevisProElement = document.getElementById("cients_devis_pro");
  var selectDevisProOption = selectDevisProElement.options[selectDevisProElement.selectedIndex];
  var selectedDevisProValue = selectDevisProOption.value;
  let formData = new FormData();
  var radios = document.getElementsByName('mode_emp');
  var radio_value;
  for (var i = 0; i < radios.length; i++) {
    // Check if the radio button is checked
    if (radios[i].checked) {
      // If checked, log its value
      radio_value = radios[i].value;
      break;
    }
  }
  if (selectedDevisProValue != -1) {
    formData.append('client_id', selectedDevisProValue);

  }
  var file_btn = document.getElementById("file_btn");
  // text_bn.classList.add("active-case");
  if (radio_value == "livraison") {
    var prix_livr_ht;
    if (file_btn.classList.contains("active-case")) {
      prix_livr_ht = parseFloat(document.getElementById("prix_livr_ht").innerHTML);
    } else {
      prix_livr_ht = parseFloat(document.getElementById("prix_livr_text_ht").innerHTML);
    }
    formData.append('prix_livr_ht', prix_livr_ht);
  }
  var selectMatiereElement = document.getElementById("matiere_select");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var matiere = selectedMatiereOption.innerText;

  var selectTypeElement = document.getElementById("type_matiere");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var type_matiere = selectedTypeOption.innerText;

  var selectEpesseurElement = document.getElementById("epp");
  var selectEpesseuredOption = selectEpesseurElement.options[selectEpesseurElement.selectedIndex];
  var epp = selectEpesseuredOption.innerText;
  var selectType = document.getElementById("type_usinage");
  var selectedTypeOption = selectType.options[selectType.selectedIndex];
  var type_usinage = selectedTypeOption.innerText;

  var prix_ht = parseFloat(document.getElementById("prix_lin_ht").innerHTML);
  // var prix_limeaire = document.getElementById("frais_decoup_ttc").innerHTML;
  if (file_btn.classList.contains("active-case")) {
    if (matiere == "Newbond") {

      let selects = document.querySelectorAll('#plaque_div select');
      if (selects.length) {
        let selectedValues = [];
        let selectedQte = [];
        let input = "";
        let value = 0;
        selects.forEach(function (select) {
          value = select.value;
          let text = select.selectedOptions[0].text;

          selectedValues.push(text);
          input = select.nextElementSibling;
          selectedQte.push(input.querySelector('input.qte_plaque').value);

        });

        formData.append('plaques', selectedValues);
        formData.append('qte_plaques', selectedQte);
      }
    }

  }
  var qte = parseInt(document.getElementById("qte").value);
  console.log(prix_ht);
  formData.append('name_matiere', matiere);
  formData.append('type_matiere', type_matiere);

  formData.append('type_usinage', type_usinage);
  formData.append('qte', qte);
  formData.append('prix_ht', prix_ht);
  formData.append('epaisseur', epp);
  formData.append('user', user);
  if (!file_btn.classList.contains("active-case")) {

    var selectHauteurElement = document.getElementById("height");
    var selectHauteurOption = selectHauteurElement.options[selectHauteurElement.selectedIndex];
    var hauteur = selectHauteurOption.innerText;
    var nbr_lettres = document.getElementById("nbr_lettres").innerHTML;
    var prix_pu = document.getElementById("prix_lettre_ht").innerHTML;
    formData.append('hauteur', hauteur);
    formData.append('nbr_lettres', nbr_lettres);
    formData.append('prix_pu', prix_pu);
  }


  $.ajax({
    url: '/telecharger_pdf',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (src_pdf) {
      ;
      console.log(src_pdf["path"]);
      var link = document.createElement('a');
      link.href = src_pdf["path"] + '/output.pdf';
      link.download = 'devis.pdf';
      document.body.appendChild(link);
      console.log(link)
      link.click();
      document.body.removeChild(link);

    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}

function telecharger_dxf(path_folder, name) {
  var link = document.createElement('a');
  console.log(path_folder + '/DXF/' + name + '.dxf');
  link.href = path_folder + '/DXF/' + name + '.dxf';  // Replace with the actual path to your PDF file.
  link.download = 'dxf_file.png';  // The name you want the downloaded file to have.
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
function telecharger_bc(path_folder, name) {
  var link = document.createElement('a');
  console.log(path_folder + '/BL/' + name + '.pdf');
  link.href = path_folder + '/BL/' + name + '.pdf';  // Replace with the actual path to your PDF file.
  link.download = 'bl_file.pdf';  // The name you want the downloaded file to have.
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
function telecharger_bc_fin(path_folder, name) {
  var link = document.createElement('a');
  console.log(path_folder + '/BL/' + name + '.pdf');
  link.href = path_folder + '/BL/' + name + '.pdf';  // Replace with the actual path to your PDF file.
  link.download = 'bl_file.pdf';  // The name you want the downloaded file to have.
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
// function confirmation(id) {
//   let formData = new FormData();
//   formData.append("id", id);
//   $.ajax({
//     url: '/change_statut_confirmer',
//     type: 'POST',
//     data: formData,
//     contentType: false,
//     processData: false,
//     success: function (msg) {
//       window.location.href = "/en_attente";

//       // Change the image source
//       //  imageElement.src =  'static/img/upload/current.png';
//       //  let myDiv = document.getElementById("accordionExample");
//       //  myDiv.style.display = "block";
//       // let myDiv2 = document.getElementById("prix_total");
//       // myDiv2.style.display = "block";

//     },
//     error: function () {
//       alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
//     }
//   });
// }
function usiner(id, path, name) {
  var selectFormElement = document.getElementById("form_select");
  var selectedFormOption = selectFormElement.options[selectFormElement.selectedIndex];
  var plaque = selectedFormOption.innerText;
  var qte_plaque = document.getElementById("qte_plaque").value;
  let formData = new FormData();
  const selectElement = document.getElementById('mySelect');
  const selectedValues = [];

  for (let i = 0; i < selectElement.options.length; i++) {
    if (selectElement.options[i].selected) {
      selectedValues.push(selectElement.options[i].innerHTML);
    }
  }

  const selectElementEmplacement = document.getElementById('enpl_select');
  const selectedValuesEmplacement = [];

  for (let i = 0; i < selectElementEmplacement.options.length; i++) {
    if (selectElementEmplacement.options[i].selected) {
      selectedValuesEmplacement.push(selectElementEmplacement.options[i].innerHTML);
    }
  }


  formData.append("id", id);
  formData.append("path", path);
  formData.append("name", name);
  formData.append("plaque", plaque);
  formData.append("qte_plaque", qte_plaque);
  formData.append("selectedValues", selectedValues);
  formData.append("selectedValuesEmplacement", selectedValuesEmplacement);
  $.ajax({
    url: '/change_statut_usiner',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {
      window.location.href = "/confirme";

      //     // Change the image source
      //     //  imageElement.src =  'static/img/upload/current.png';
      //     //  let myDiv = document.getElementById("accordionExample");
      //     //  myDiv.style.display = "block";
      //     // let myDiv2 = document.getElementById("prix_total");
      //     // myDiv2.style.display = "block";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });
}
function text_btn_active() {

  var file_btn = document.getElementById("file_btn");
  var text_bn = document.getElementById("text_btn");

  // text_bn.classList.add("active-case");
  if (!text_bn.classList.contains("active-case")) {

    text_bn.classList.add("active-case");
    text_section = document.getElementById("text-section");
    text_section.style.display = "block"
    if (document.getElementById("section_surface_usinage").style.display == "block") {
      document.getElementById("section_surface_usinage").style.display = "none";
    }
    let labels = document.getElementsByClassName("label");
    document.getElementById("qte").value = 1;
    // Iterate through each element and set the display property to "block"
    for (let i = 0; i < labels.length; i++) {
      labels[i].style.display = "none";
    }

    if (file_btn.classList.contains("active-case")) {
      file_btn.classList.remove("active-case");
      drop_area = document.getElementById("drop-area");
      drop_area.style.display = "none";
      img_usinage = document.getElementById('img_usinage');
      img_usinage.style.display = 'none'
      text_div = document.getElementById("text_div");
      text_div.style.display = 'block';

    }

    $.ajax({
      url: '/charge_text_data',
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
        var selectMatiereElement = document.getElementById("matiere_select");
        var selectTypeElement = document.getElementById("type_matiere");
        var selectEpaisseurElement = document.getElementById("epp");
        var selectTypeUsinageElement = document.getElementById("type_usinage");
        var selectHauteurElement = document.getElementById("height");
        while (selectMatiereElement.options.length > 0) {
          selectMatiereElement.remove(0);
        }
        const length_matieres = data["matieres"].length;

        for (let i = 0; i < length_matieres; i++) {
          console.log(data["matieres"][i].name);
          const newOption = document.createElement('option');
          newOption.value = data["matieres"][i].id;
          newOption.text = data["matieres"][i].name;
          selectMatiereElement.add(newOption);
        }

        while (selectTypeElement.options.length > 0) {
          selectTypeElement.remove(0);
        }
        const length_matieres_types = data["types"].length;

        for (let i = 0; i < length_matieres_types; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types"][i].id;
          newOption.text = data["types"][i].name;
          selectTypeElement.add(newOption);
        }
        while (selectEpaisseurElement.options.length > 0) {
          selectEpaisseurElement.remove(0);
        }


        const length_arr = data["epaisseurs"].length;
        for (let i = 0; i < length_arr; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["epaisseurs"][i].id;
          newOption.text = data["epaisseurs"][i].value;
          selectEpaisseurElement.add(newOption);
        }

        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usg = data["types_usinage"].length;
        for (let i = 0; i < length_usg; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }

        while (selectHauteurElement.options.length > 0) {
          selectHauteurElement.remove(0);
        }
        const length_hauteur = data["hauteurs"].length;

        for (let i = 0; i < length_hauteur; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["hauteurs"][i].id;
          newOption.text = data["hauteurs"][i].value / 10;
          selectHauteurElement.add(newOption);
        }
        document.getElementById("prix_detailles").style.display = "none";
        document.getElementById("total_prix_detailles").style.display = "none";
        let verif_file = document.getElementById("fileInput");
        if (verif_file.value) {
          verif_file.value = "";
          var iframe = document.getElementById('img_usinage');
          iframe.src = 'static/img/usinage/matiers/Pvc.jpg';
        }
      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }


}

function upload_btn_active() {

  var file_btn = document.getElementById("file_btn");
  var text_bn = document.getElementById("text_btn");

  // text_bn.classList.add("active-case");
  if (!file_btn.classList.contains("active-case")) {

    file_btn.classList.add("active-case");
    drop_area = document.getElementById("drop-area");
    drop_area.style.display = "block"
    document.getElementById("qte").value = 1;

    if (text_bn.classList.contains("active-case")) {
      text_bn.classList.remove("active-case");
      text_section = document.getElementById("text-section");
      text_section.style.display = "none";
      img_usinage = document.getElementById('img_usinage');
      img_usinage.style.display = 'block'
      text_div = document.getElementById("text_div");
      text_div.style.display = 'none';
    }

    $.ajax({
      url: '/charge_form_data',
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data);
        var selectMatiereElement = document.getElementById("matiere_select");
        var selectTypeElement = document.getElementById("type_matiere");
        var selectEpaisseurElement = document.getElementById("epp");
        var selectTypeUsinageElement = document.getElementById("type_usinage");
        while (selectMatiereElement.options.length > 0) {
          selectMatiereElement.remove(0);
        }
        const length_matieres = data["matieres"].length;

        for (let i = 0; i < length_matieres; i++) {
          console.log(data["matieres"][i].name);
          const newOption = document.createElement('option');
          newOption.value = data["matieres"][i].id;
          newOption.text = data["matieres"][i].name;
          selectMatiereElement.add(newOption);
        }

        while (selectTypeElement.options.length > 0) {
          selectTypeElement.remove(0);
        }
        const length_matieres_types = data["types"].length;

        for (let i = 0; i < length_matieres_types; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types"][i].id;
          newOption.text = data["types"][i].name;
          selectTypeElement.add(newOption);
        }
        while (selectEpaisseurElement.options.length > 0) {
          selectEpaisseurElement.remove(0);
        }


        const length_arr = data["epaisseurs"].length;
        for (let i = 0; i < length_arr; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["epaisseurs"][i].id;
          newOption.text = data["epaisseurs"][i].value;
          selectEpaisseurElement.add(newOption);
        }

        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usg = data["types_usinage"].length;
        for (let i = 0; i < length_usg; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }
        document.getElementById("prix_detailles").style.display = "none";
        document.getElementById("total_prix_detailles").style.display = "none";
        document.getElementById("text_input").value = "";
        document.getElementById("text_area").innerHTML = "";


      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });
  }
}

function forms_btn_active() {

  var file_btn = document.getElementById("file_btn");
  var text_bn = document.getElementById("text_btn");

  // text_bn.classList.add("active-case");
  if (!file_btn.classList.contains("active-case")) {

    file_btn.classList.add("active-case");
    drop_area = document.getElementById("drop-area");
    drop_area.style.display = "block"


    if (text_bn.classList.contains("active-case")) {
      text_bn.classList.remove("active-case");
      text_section = document.getElementById("text-section");
      text_section.style.display = "none";
    }

    $.ajax({
      url: '/charge_form_data',
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
        console.log(data);
        var selectMatiereElement = document.getElementById("matiere_select");
        var selectTypeElement = document.getElementById("type_matiere");
        var selectEpaisseurElement = document.getElementById("epp");
        var selectTypeUsinageElement = document.getElementById("type_usinage");
        while (selectMatiereElement.options.length > 0) {
          selectMatiereElement.remove(0);
        }
        const length_matieres = data["matieres"].length;

        for (let i = 0; i < length_matieres; i++) {
          console.log(data["matieres"][i].name);
          const newOption = document.createElement('option');
          newOption.value = data["matieres"][i].id;
          newOption.text = data["matieres"][i].name;
          selectMatiereElement.add(newOption);
        }

        while (selectTypeElement.options.length > 0) {
          selectTypeElement.remove(0);
        }
        const length_matieres_types = data["types"].length;

        for (let i = 0; i < length_matieres_types; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types"][i].id;
          newOption.text = data["types"][i].name;
          selectTypeElement.add(newOption);
        }
        while (selectEpaisseurElement.options.length > 0) {
          selectEpaisseurElement.remove(0);
        }


        const length_arr = data["epaisseurs"].length;
        for (let i = 0; i < length_arr; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["epaisseurs"][i].id;
          newOption.text = data["epaisseurs"][i].value;
          selectEpaisseurElement.add(newOption);
        }

        while (selectTypeUsinageElement.options.length > 0) {
          selectTypeUsinageElement.remove(0);
        }
        const length_usg = data["types_usinage"].length;
        for (let i = 0; i < length_usg; i++) {
          const newOption = document.createElement('option');
          newOption.value = data["types_usinage"][i].id;
          newOption.text = data["types_usinage"][i].name;
          selectTypeUsinageElement.add(newOption);
        }

      },
      error: function () {
        alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
      }
    });
  }
}
function ajuter_plaque_select() {
  let formData = new FormData();
  var selectMatiereElement = document.getElementById("matiere_select");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var selectedMatiereValue = selectedMatiereOption.value;
  var matiereText = selectedMatiereOption.innerHTML;

  var selectTypeElement = document.getElementById("type_matiere");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;

  var selectEpaisseurElement = document.getElementById("epp");
  var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
  var selectedEpaisseurValue = selectedEpaisseurOption.value;

  formData.append('matiere_id', selectedMatiereValue);
  formData.append('type_id', selectedTypeValue);
  formData.append('epaisseur_id', selectedEpaisseurValue);

  $.ajax({
    url: '/get_plaques_usinage',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {

      var myDiv = document.getElementById("plaque_div");
      if (data["plaques"].length > 0) {
        var htmlCode = `
          <div class=" mt-3 row select_plaque_div">
            <select class=" col col-md-5 form-select select-plaque " aria-label="select plaques" style="  width: 60%;" onchange="selectOptionChanged()">`;

        for (let i = 0; i < data["plaques"].length; i++) {
          htmlCode += `<option value=` + data["plaques"][i]["prix_plaque"] + `>` + data["plaques"][i]["dimonsion_plaque"] + `</option>`;
        }

        htmlCode += `
            </select>
         
          <div class="col col-md-4">
            <button class="btn_counter decrement_plaque_surface" onclick="decrementPlaqueSurface(this)">-</button>
            <input class="qte_plaque" value="1" min="0"  oninput="change_input_plaque_surface(this)" >
            <button class="btn_counter increment_plaque_surface" onclick="incrimentPlaqueSurface(this)">+</button>
          </div>
           </div>`;

        // Utilisez insertAdjacentHTML pour ajouter le nouveau contenu sans remplacer l'existant
        myDiv.insertAdjacentHTML('beforeend', htmlCode);
        checkPlaquesValues();

      }
    },
    error: function () {
      alert('Une erreur s\'est produite lors de faire l\'opération.');
    }
  });

}
function selectOptionChanged() {
  checkPlaquesValues();
}
function checkPlaquesValues() {
  var selects = document.querySelectorAll('#plaque_div select');
  var selectedValues = [];
  var selectedSurface = [];
  var selectedQte = [];
  var input2 = "";
  let width, height, current_surface = 0;
  let parts = [];
  var qte = parseFloat(document.getElementById("qte").value);
  var nbr_percage = parseInt(document.getElementById("qte_percage").innerHTML);
  let frais_decoup_ht = parseFloat(document.getElementById("frais_decoup_ht").innerHTML);
  selects.forEach(function (select) {
    let value = select.value;
    let text = select.selectedOptions[0].text;
    parts = text.split('x');
    // // Convert the parts to floating-point numbers

    width = (parseFloat(parts[0]) - 20) / 1000;
    height = (parseFloat(parts[1]) - 20) / 1000;
    current_surface = (width * height).toFixed(2);

    console.log(current_surface);
    selectedSurface.push(current_surface);
    selectedValues.push(value);
    input2 = select.nextElementSibling;

    selectedQte.push(input2.querySelector('input.qte_plaque').value);

  });
  console.log(selectedSurface);
  console.log(selectedValues);
  var result_surface = 0;
  var result_prix = 0;
  for (let i = 0; i < selectedSurface.length; i++) {

    result_surface += parseFloat(selectedSurface[i]) * parseFloat(selectedQte[i]);
    result_prix += parseFloat(selectedValues[i]) * parseFloat(selectedQte[i]);
  }

  let value_surface_chutes = parseFloat(document.getElementById("surface_usinage_hidden").innerText);
  if (value_surface_chutes < result_surface) {
    document.getElementById("add_new_plaque").style.display = "none";
    document.getElementById("surface_usinage").innerHTML = 0;

  } else {
    document.getElementById("add_new_plaque").style.display = "block";
    document.getElementById("surface_usinage").innerHTML = (value_surface_chutes - result_surface).toFixed(2);
  }
  let prix_matiere_chute = parseFloat(document.getElementById("prix_matiere_hidden").innerHTML);
  let surface_chutes = parseFloat(document.getElementById("surface_usinage").innerHTML);
  let prix_matiere_ht = result_prix + surface_chutes * prix_matiere_chute;
  let prix_matiere_ttc = 1.2 * prix_matiere_ht;
  let prix_total_ht = qte * (prix_matiere_ht + frais_decoup_ht + 0.3 * nbr_percage);
  let prix_total_ttc = 1.2 * prix_total_ht;
  document.getElementById("prix_lin_ht").innerHTML = prix_total_ht.toFixed(2);
  document.getElementById("prix_lin_ttc").innerHTML = prix_total_ttc.toFixed(2);
  document.getElementById("prix_mat_ht").innerHTML = prix_matiere_ht.toFixed(2);
  document.getElementById("prix_mat_ttc").innerHTML = prix_matiere_ttc.toFixed(2);
}
// ouvre nes user form
function newClientForm() {
  var liste_clients_section = document.getElementById("liste_clients_section");
  liste_clients_section.style.display = "flex";
  // var selectRepresentant = document.getElementById("representant");
  // var selectedRepresentantValue= selectRepresentant.value;
  // var selectedRepresentantText = selectRepresentant.innerHTML;
  // var selectEpaisseurElement = document.getElementById("epp");
  // var selectRepresentantOption = selectRepresentant.options[selectRepresentant.selectedIndex];
  // var selectedRepresentantValue = selectRepresentantOption.value;
  // var selectedRepresentantText = selectRepresentantOption.innerHTML;

  // var rep_new_client = document.getElementById("rep_new_client");
  // rep_new_client.options[0].value=selectedRepresentantValue;
  // rep_new_client.options[0].innerHTML=selectedRepresentantText;

  // var opp = rep_new_client.options[rep_new_client.selectedIndex];
  // var testValue = opp.value;
  // var testText = opp.innerHTML;
  // console.log(testText);
}

// fermer Form

function closeFormClient() {

  var liste_clients_section = document.getElementById("liste_clients_section");
  liste_clients_section.style.display = "none";
}

function addNewClient() {
  var selectRepresentantElement = document.getElementById("rep_new_client");
  var selectRepresentantOption = selectRepresentantElement.options[selectRepresentantElement.selectedIndex];
  var selectedRepresentantValue = selectRepresentantOption.value;

  var name = document.getElementById("name");
  var nameText = name.value;
  var numeroVoie = document.getElementById("numero_voie");
  var numeroVoieText = numeroVoie.value;

  var nameVoie = document.getElementById("nom_voie");
  var nameVoieText = nameVoie.value;

  var cp = document.getElementById("cp");
  var cpText = cp.value;

  var ville = document.getElementById("ville");
  var villeText = ville.value;

  var email = document.getElementById("email_new_client");
  var emailText = email.value;

  var prix_clent_livr = document.getElementById("prix_clent_livr").value;
  var telp = document.getElementById("telp");
  var telpText = telp.value;



  let formData = new FormData();
  formData.append('representant', selectedRepresentantValue);
  formData.append('name', nameText);
  formData.append('numeroVoie', numeroVoieText);
  formData.append('nameVoie', nameVoieText);
  formData.append('cp', cpText);
  formData.append('ville', villeText);
  formData.append('email', emailText);
  formData.append('prix_clent_livr', prix_clent_livr);
  formData.append('tel', telpText);
  //  else if (!validateEmail(email)) {
  //     msg = "Respecter les règles  pour rédiger un mail!"
  var msg = "";
  if (isAnyFormDataEmpty(formData)) {
    msg = "Un ou plusieurs champs du formulaire sont vides";
  } else if (isNumber(numeroVoie) || numeroVoie <= 0) {
    msg = "Numéro de voie doit être supérieur à 0";
  } else if (isNumber(cp) || cp <= 0) {
    msg = "CP  doit être supérieur à 0";
  } else if (isNumber(cp) || cp <= 0) {
    msg = "CP  doit être supérieur à 0";
  }



  if (msg === "") {
    $.ajax({
      url: '/new_client',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        console.log(msg)
        var liste_clients_section = document.getElementById("liste_clients_section");
        liste_clients_section.style.display = "none";
        window.location.href = "/clients";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });

  } else {
    alert("é");
    var errorMessage = document.getElementById('msg_div');
    errorMessage.style.display = 'block';
    document.getElementById("msg_div").innerHTML = "Respecter les règles  pour rédiger un mail!"
    setTimeout(() => {
      errorMessage.style.display = 'none';
    }, 1500);
  }

}

$('#clients_table').on('click', function (event) {


  // Check if the clicked element is a button with the class 'getInfoBtn'
  if (event.target.classList.contains('getInfoBtn')) {
    var liste_clients_section = document.getElementById("edit_client_section");
    liste_clients_section.style.display = "flex";
    // Find the parent row (tr) of the clicked button
    const row = event.target.closest('tr');
    var rec_user_id = row.querySelector('.rec_user_id').textContent;
    var rec_client_id = row.querySelector('.rec_client_id').textContent;
    // Get data from the row
    var id = row.cells[0].value;
    var name_rep = row.cells[1].innerText;
    var name_client = row.cells[2].innerText;

    var numero_voie_span = row.querySelector('.numero_voie_edit_span');
    var name_voie_span = row.querySelector('.name_voie_edit_span');

    // Get the value from the span element
    var numero_voie_value = numero_voie_span.textContent.trim();
    var name_voie_value = name_voie_span.textContent.trim();

    var selectElement = document.getElementById("rep_edit_client");
    // Loop through options to find the one with the desired value
    for (var i = 0; i < selectElement.options.length; i++) {
      if (selectElement.options[i].selected == true) {
        // Set the selected property to true for the found option
        selectElement.options[i].innerHTML = name_rep;
        selectElement.options[i].value = rec_user_id;

        break;
      }
    }
    var cp = row.cells[4].innerText;



    var ville = row.cells[5].innerText;
    var email = row.cells[6].innerText;
    var tel = row.cells[8].innerText;
    var prix_livr = row.cells[7].innerText;


    document.getElementById("name_client_edit").value = name_client;
    document.getElementById("numero_voie_edit").value = numero_voie_value;
    document.getElementById("nom_voie_edit").value = name_voie_value;

    document.getElementById("cp_edit").value = cp;
    document.getElementById("ville_edit").value = ville;
    document.getElementById("email_edit").value = email;
    document.getElementById("telp_edit").value = tel;
    document.getElementById("rec_client_id").innerHTML = rec_client_id;
    document.getElementById("client_edit_prix_livr").value = prix_livr;

  }
});

function closeEditClient() {
  var liste_clients_section = document.getElementById("edit_client_section");
  liste_clients_section.style.display = "none";
}

function EnregistrerEditClient() {
  var selectRepresentantElement = document.getElementById("rep_edit_client");
  var selectRepresentantOption = selectRepresentantElement.options[selectRepresentantElement.selectedIndex];
  var selectedRepresentantValue = selectRepresentantOption.value;
  console.log(selectedRepresentantValue);
  var name = document.getElementById("name_client_edit");
  var nameText = name.value;

  var client_id = document.getElementById("rec_client_id").value;



  var numeroVoie = document.getElementById("numero_voie_edit");
  var numeroVoieText = numeroVoie.value;

  var nameVoie = document.getElementById("nom_voie_edit");
  var nameVoieText = nameVoie.value;

  var cp = document.getElementById("cp_edit");
  var cpValue = cp.value;


  var ville = document.getElementById("ville_edit");
  var villeText = ville.value;

  var email = document.getElementById("email_edit");
  var emailText = email.value;

  var telp = document.getElementById("telp_edit");
  var telpText = telp.value;

  var livraison = document.getElementById("client_edit_prix_livr");
  var prix_livr = client_edit_prix_livr.value;
  let formData = new FormData();
  formData.append('representant', selectedRepresentantValue);
  formData.append('name', nameText);
  formData.append('numeroVoie', numeroVoieText);
  formData.append('nameVoie', nameVoieText);
  formData.append('cp', cpValue);
  formData.append('ville', villeText);
  formData.append('email', emailText);
  formData.append('tel', telpText);
  formData.append('client_id', client_id);
  formData.append('prix_livr', prix_livr);
  console.log(selectedRepresentantValue);
  console.log(client_id);
  console.log(telpText);
  console.log(emailText);
  console.log(villeText);
  console.log(cpValue);
  console.log(nameVoieText);
  console.log(nameText);


  $.ajax({
    url: '/edit_client',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (msg) {

      console.log(msg)
      var liste_clients_section = document.getElementById("edit_client_section");
      liste_clients_section.style.display = "none";
      window.location.href = "/clients";

    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });



  // var selectedRepresentantText = selectRepresentantOption.innerHTML;
  // console.log(selectedRepresentantText);
}


$('#matieres_table').on('change', function (event) {
  var confirmed = confirm("Voulez-vous enregistrer les modifications ?");


  if (event.target.classList.contains('prix_limeaire_input')) {
    if (confirmed) {
      const row = event.target.closest('tr');
      var newValue = row.querySelector('.prix_limeaire_input').value;
      console.log(row);
      // var rec_user_id = row.querySelector('.rec_user_id').textContent;
      // var rec_client_id = row.querySelector('.rec_client_id').textContent;
      // Get data from the row
      var matiere = row.cells[1].innerHTML;
      var type = row.cells[2].innerHTML;
      var type_usinage = row.cells[3].innerHTML;
      var epaisseur = row.cells[4].innerHTML;
      console.log(matiere);
      console.log(type);
      console.log(type_usinage);
      console.log(epaisseur);
      let formData = new FormData();
      formData.append('new_prix_limeaire', newValue);
      formData.append('matiere', matiere);
      formData.append('type_matiere', type);
      formData.append('type_usinage', type_usinage);
      formData.append('epaisseur', epaisseur);
      $.ajax({
        url: '/edit_prix_limeaire',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (msg) {

          console.log(msg)
          // var liste_clients_section = document.getElementById("edit_client_section");
          // liste_clients_section.style.display = "none";
          // window.location.href = "/clients";

        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    }
  } else if (event.target.classList.contains('prix_matiere_input')) {
    if (confirmed) {
      const row = event.target.closest('tr');
      var newValue = row.querySelector('.prix_matiere_input').value;
      var matiere = row.cells[1].innerHTML;
      var type = row.cells[2].innerHTML;
      var type_usinage = row.cells[3].innerHTML;
      var epaisseur = row.cells[4].innerHTML;
      let formData = new FormData();
      formData.append('new_prix_matiere', newValue);
      formData.append('matiere', matiere);
      formData.append('type_matiere', type);
      formData.append('type_usinage', type_usinage);
      formData.append('epaisseur', epaisseur);
      $.ajax({
        url: '/edit_prix_matiere',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (msg) {

          console.log(msg)
          // var liste_clients_section = document.getElementById("edit_client_section");
          // liste_clients_section.style.display = "none";
          // window.location.href = "/clients";

        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });

    }
  }
});

function delete_client(current_row, id) {
  let text = "Attention!En supprimant cette client ,ca va supprimer automatiquement tous les commandes en cours de  cette client.Voulez vous supprimer la cliente?";
  if (confirm(text)) {
    let formData = new FormData();
    formData.append('id_client', id);
    $.ajax({
      url: '/delete_client',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        var row = current_row.parentNode.parentNode; // Get the parent row of the button
        row.parentNode.removeChild(row); // Remove the row from the table
        // var liste_clients_section = document.getElementById("edit_client_section");
        // liste_clients_section.style.display = "none";
        // window.location.href = "/clients";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }
}

function delete_selected_user(current_row, id) {
  let text = "Attention!En supprimant cette user ,ca va supprimer automatiquement tous les  clients et les commandes en cours de lies avec  cette client.Voulez vous supprimer la cliente?";
  alert(id);
  if (confirm(text)) {
    console.log("ttttttttttttt");
    console.log(id);
    alert("sd");
    let formData = new FormData();
    formData.append('id_user', id);
    $.ajax({
      url: '/delete_user',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        var row = current_row.parentNode.parentNode; // Get the parent row of the button
        row.parentNode.removeChild(row); // Remove the row from the table
        // var liste_clients_section = document.getElementById("edit_client_section");
        // liste_clients_section.style.display = "none";
        // window.location.href = "/clients";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }
}

function delete_bridge_row(current_bridge_row) {
  let text = "Attention!En supprimant cette client ,ca va supprimer automatiquement tous les commandes en cours de  ces informations.Voulez vous supprimer la cliente?";
  if (confirm(text)) {
    var row = current_bridge_row.parentNode.parentNode;
    var matiere = row.cells[1].innerHTML;
    var type = row.cells[2].innerHTML;
    var usinage = row.cells[3].innerHTML;
    var epaisseur = row.cells[4].innerHTML;


    let formData = new FormData();
    formData.append('matiere', matiere);
    formData.append('type', type);
    formData.append('usinage', usinage);
    formData.append('epaisseur', epaisseur);
    console.log(matiere);
    console.log(type);
    console.log(usinage);
    console.log(epaisseur);
    $.ajax({
      url: '/delete_bridge_row',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        console.log(msg);

        row.parentNode.removeChild(row);
        // Get the parent row of the button
        // row.parentNode.removeChild(row); // Remove the row from the table
        // var liste_clients_section = document.getElementById("edit_client_section");
        // liste_clients_section.style.display = "none";
        // window.location.href = "/clients";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }
}

function lettres_btn_bridge_active() {
  $.ajax({
    url: '/charge_text_prix_data',
    type: 'POST',
    contentType: false,
    processData: false,
    success: function (data) {
      var current_user_role = document.getElementById("output_user_role").innerHTML;
      var selectMatiereElement = document.getElementById("matiere_list_text");
      var selectTypeElement = document.getElementById("type_list_text");
      var selectEpaisseurElement = document.getElementById("epaisseur_text");
      // var selectTypeUsinageElement = document.getElementById("type_usinage");
      // var selectHauteurElement = document.getElementById("height");
      while (selectMatiereElement.options.length > 0) {
        selectMatiereElement.remove(0);
      }
      const length_matieres = data["matieres"].length;

      for (let i = 0; i < length_matieres; i++) {
        console.log(data["matieres"][i].name);
        const newOption = document.createElement('option');
        newOption.value = data["matieres"][i].id;
        newOption.text = data["matieres"][i].name;
        selectMatiereElement.add(newOption);
      }

      while (selectTypeElement.options.length > 0) {
        selectTypeElement.remove(0);
      }
      const length_matieres_types = data["types"].length;

      for (let i = 0; i < length_matieres_types; i++) {
        const newOption = document.createElement('option');
        newOption.value = data["types"][i].id;
        newOption.text = data["types"][i].name;
        selectTypeElement.add(newOption);
      }
      while (selectEpaisseurElement.options.length > 0) {
        selectEpaisseurElement.remove(0);
      }


      const length_arr = data["epaisseurs"].length;
      for (let i = 0; i < length_arr; i++) {
        const newOption = document.createElement('option');
        newOption.value = data["epaisseurs"][i].id;
        newOption.text = data["epaisseurs"][i].value;
        selectEpaisseurElement.add(newOption);
      }

      // while (selectTypeUsinageElement.options.length > 0) {
      //   selectTypeUsinageElement.remove(0);
      // }
      // const length_usg = data["types_usinage"].length;
      // for (let i = 0; i < length_usg; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["types_usinage"][i].id;
      //   newOption.text = data["types_usinage"][i].name;
      //   selectTypeUsinageElement.add(newOption);
      // }

      // while (selectHauteurElement.options.length > 0) {
      //   selectHauteurElement.remove(0);
      // }
      // const length_hauteur = data["hauteurs"].length;

      // for (let i = 0; i < length_hauteur; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["hauteurs"][i].id;
      //   newOption.text = data["hauteurs"][i].value / 10 + " cm";
      //   selectHauteurElement.add(newOption);
      // }


      var table = document.getElementById("matieres_text_table");
      var rowCount = table.rows.length;

      // Start from the last row and remove each one
      for (var i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
      }

      var nbr = 1;
      for (var i = 0; i < data['prix_lettre_list'].length; i++) {
        console.log(data["prix_lettre_list"][i]);

        var row = table.insertRow();
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6);
        if (current_user_role === "admin") {
          var cell7 = row.insertCell(7);
        }


        cell0.innerHTML = nbr++;
        cell1.innerHTML = data["prix_lettre_list"][i]["matiere_name"];
        cell2.innerHTML = data["prix_lettre_list"][i]["type_name"];
        cell3.innerHTML = data["prix_lettre_list"][i]["usinage_name"];
        cell4.innerHTML = data["prix_lettre_list"][i]["epaisseur_value"];
        cell5.innerHTML = data["prix_lettre_list"][i]["hauteur_value"] / 10;

        if (current_user_role === "admin") {
          cell6.innerHTML = `<input type="text" value='` + data["prix_lettre_list"][i]["prix"] + `'class='prix_text_input'>€`;
          cell7.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                  onclick="delete_Lettrebridge_row(this)"></i>
            `;
        } else {
          cell6.innerHTML = `<output type="text" >` + data["prix_lettre_list"][i]["prix"] + ` € </output>`;
        }
      }
      var text_section = document.getElementById("text_section");
      text_section.style.display = "block";
      var form_section = document.getElementById("form_section");
      form_section.style.display = "none";
      var epaisseur_text_div = document.getElementById("epaisseur_text_div");
      epaisseur_text_div.style.display = "block";
    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });

}

function forms_btn_bridge_active() {

  var text_section = document.getElementById("text_section");
  text_section.style.display = "none";
  var form_section = document.getElementById("form_section");
  form_section.style.display = "block";
  var epaisseur_text_div = document.getElementById("epaisseur_text_div");
  epaisseur_text_div.style.display = "none";
  window.location.href = "/prix";

}

$("#matiere_list_text").on('change', function () {
  var current_user_role = document.getElementById("output_user_role").innerHTML;
  let formData = new FormData();
  var selectMatiereElement = document.getElementById("matiere_list_text");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var selectedMatiereValue = selectedMatiereOption.value;


  var selectTypeElement = document.getElementById("type_list_text");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;

  var selectEpaisseurElement = document.getElementById("epaisseur_text");
  var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
  var selectedEpaisseurValue = selectedEpaisseurOption.value;


  formData.append('matiere_id', selectedMatiereValue);
  // formData.append('type_id', selectedTypeValue);




  $.ajax({
    url: '/matieres_text_liste',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {

      while (selectTypeElement.options.length > 0) {
        selectTypeElement.remove(0);
      }
      const length_matieres_types = data["types"].length;

      for (let i = 0; i < length_matieres_types; i++) {
        const newOption = document.createElement('option');
        newOption.value = data["types"][i].id;
        newOption.text = data["types"][i].name;
        selectTypeElement.add(newOption);
      }
      while (selectEpaisseurElement.options.length > 0) {
        selectEpaisseurElement.remove(0);
      }


      const length_arr = data["epaisseurs"].length;
      for (let i = 0; i < length_arr; i++) {
        const newOption = document.createElement('option');
        newOption.value = data["epaisseurs"][i].id;
        newOption.text = data["epaisseurs"][i].value;
        selectEpaisseurElement.add(newOption);
      }

      // while (selectTypeUsinageElement.options.length > 0) {
      //   selectTypeUsinageElement.remove(0);
      // }
      // const length_usg = data["types_usinage"].length;
      // for (let i = 0; i < length_usg; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["types_usinage"][i].id;
      //   newOption.text = data["types_usinage"][i].name;
      //   selectTypeUsinageElement.add(newOption);
      // }

      // while (selectHauteurElement.options.length > 0) {
      //   selectHauteurElement.remove(0);
      // }
      // const length_hauteur = data["hauteurs"].length;

      // for (let i = 0; i < length_hauteur; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["hauteurs"][i].id;
      //   newOption.text = data["hauteurs"][i].value / 10 + " cm";
      //   selectHauteurElement.add(newOption);
      // }


      var table = document.getElementById("matieres_text_table");
      var rowCount = table.rows.length;

      // Start from the last row and remove each one
      for (var i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
      }

      var nbr = 1;
      for (var i = 0; i < data['prix_lettre_list'].length; i++) {

        var row = table.insertRow();
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6);
        if (current_user_role === "admin") {
          var cell7 = row.insertCell(7);
        }


        cell0.innerHTML = nbr++;
        cell1.innerHTML = data["prix_lettre_list"][i]["matiere_name"];
        cell2.innerHTML = data["prix_lettre_list"][i]["type_name"];
        cell3.innerHTML = data["prix_lettre_list"][i]["usinage_name"];
        cell4.innerHTML = data["prix_lettre_list"][i]["epaisseur_value"];
        cell5.innerHTML = data["prix_lettre_list"][i]["hauteur_value"] / 10;

        if (current_user_role == "admin") {
          cell6.innerHTML = `<input type="text" value='` + data["prix_lettre_list"][i]["prix"] + `'class='prix_text_input'>€`;
          cell7.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                  onclick="delete_Lettrebridge_row(this)"></i>
            `;
        } else {
          cell6.innerHTML = `<output type="text" >` + data["prix_lettre_list"][i]["prix"] + ` € </output>`;
        }
      }


    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });

});


$("#type_list_text").on('change', function () {
  var current_user_role = document.getElementById("output_user_role").innerHTML;
  let formData = new FormData();
  var selectMatiereElement = document.getElementById("matiere_list_text");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var selectedMatiereValue = selectedMatiereOption.value;


  var selectTypeElement = document.getElementById("type_list_text");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;

  var selectEpaisseurElement = document.getElementById("epaisseur_text");
  var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
  var selectedEpaisseurValue = selectedEpaisseurOption.value;


  formData.append('matiere_id', selectedMatiereValue);
  formData.append('type_id', selectedTypeValue);




  $.ajax({
    url: '/change_type_text_liste',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {

      while (selectEpaisseurElement.options.length > 0) {
        selectEpaisseurElement.remove(0);
      }


      const length_arr = data["epaisseurs"].length;
      for (let i = 0; i < length_arr; i++) {
        const newOption = document.createElement('option');
        newOption.value = data["epaisseurs"][i].id;
        newOption.text = data["epaisseurs"][i].value;
        selectEpaisseurElement.add(newOption);
      }

      // while (selectTypeUsinageElement.options.length > 0) {
      //   selectTypeUsinageElement.remove(0);
      // }
      // const length_usg = data["types_usinage"].length;
      // for (let i = 0; i < length_usg; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["types_usinage"][i].id;
      //   newOption.text = data["types_usinage"][i].name;
      //   selectTypeUsinageElement.add(newOption);
      // }

      // while (selectHauteurElement.options.length > 0) {
      //   selectHauteurElement.remove(0);
      // }
      // const length_hauteur = data["hauteurs"].length;

      // for (let i = 0; i < length_hauteur; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["hauteurs"][i].id;
      //   newOption.text = data["hauteurs"][i].value / 10 + " cm";
      //   selectHauteurElement.add(newOption);
      // }


      var table = document.getElementById("matieres_text_table");
      var rowCount = table.rows.length;

      // Start from the last row and remove each one
      for (var i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
      }

      var nbr = 1;
      for (var i = 0; i < data['prix_lettre_list'].length; i++) {
        console.log(data["prix_lettre_list"][i]);

        var row = table.insertRow();
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6);
        if (current_user_role === "admin") {
          var cell7 = row.insertCell(7);
        }


        cell0.innerHTML = nbr++;
        cell1.innerHTML = data["prix_lettre_list"][i]["matiere_name"];
        cell2.innerHTML = data["prix_lettre_list"][i]["type_name"];
        cell3.innerHTML = data["prix_lettre_list"][i]["usinage_name"];
        cell4.innerHTML = data["prix_lettre_list"][i]["epaisseur_value"];
        cell5.innerHTML = data["prix_lettre_list"][i]["hauteur_value"] / 10;

        if (current_user_role === "admin") {
          cell6.innerHTML = `<input type="text" value='` + data["prix_lettre_list"][i]["prix"] + `'class='prix_text_input'>€`;
          cell7.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                  onclick="delete_Lettrebridge_row(this)"></i>
            `;
        } else {
          cell6.innerHTML = `<output type="text">` + data["prix_lettre_list"][i]["prix"] + ` €</output>`;
        }
      }


    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });

});


$("#epaisseur_text").on('change', function () {

  var current_user_role = document.getElementById("output_user_role").innerHTML;
  let formData = new FormData();
  var selectMatiereElement = document.getElementById("matiere_list_text");
  var selectedMatiereOption = selectMatiereElement.options[selectMatiereElement.selectedIndex];
  var selectedMatiereValue = selectedMatiereOption.value;


  var selectTypeElement = document.getElementById("type_list_text");
  var selectedTypeOption = selectTypeElement.options[selectTypeElement.selectedIndex];
  var selectedTypeValue = selectedTypeOption.value;

  var selectEpaisseurElement = document.getElementById("epaisseur_text");
  var selectedEpaisseurOption = selectEpaisseurElement.options[selectEpaisseurElement.selectedIndex];
  var selectedEpaisseurValue = selectedEpaisseurOption.value;


  formData.append('matiere_id', selectedMatiereValue);
  formData.append('type_id', selectedTypeValue);
  formData.append('epaisseur_id', selectedEpaisseurValue)




  $.ajax({
    url: '/change_eppaisseur_text_liste',
    type: 'POST',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {

      // while (selectTypeUsinageElement.options.length > 0) {
      //   selectTypeUsinageElement.remove(0);
      // }
      // const length_usg = data["types_usinage"].length;
      // for (let i = 0; i < length_usg; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["types_usinage"][i].id;
      //   newOption.text = data["types_usinage"][i].name;
      //   selectTypeUsinageElement.add(newOption);
      // }

      // while (selectHauteurElement.options.length > 0) {
      //   selectHauteurElement.remove(0);
      // }
      // const length_hauteur = data["hauteurs"].length;

      // for (let i = 0; i < length_hauteur; i++) {
      //   const newOption = document.createElement('option');
      //   newOption.value = data["hauteurs"][i].id;
      //   newOption.text = data["hauteurs"][i].value / 10 + " cm";
      //   selectHauteurElement.add(newOption);
      // }


      var table = document.getElementById("matieres_text_table");
      var rowCount = table.rows.length;

      // Start from the last row and remove each one
      for (var i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
      }

      var nbr = 1;
      for (var i = 0; i < data['prix_lettre_list'].length; i++) {
        console.log(data["prix_lettre_list"][i]);

        var row = table.insertRow();
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);
        var cell5 = row.insertCell(5);
        var cell6 = row.insertCell(6);
        if (current_user_role === "admin") {
          var cell7 = row.insertCell(7);
        }


        cell0.innerHTML = nbr++;
        cell1.innerHTML = data["prix_lettre_list"][i]["matiere_name"];
        cell2.innerHTML = data["prix_lettre_list"][i]["type_name"];
        cell3.innerHTML = data["prix_lettre_list"][i]["usinage_name"];
        cell4.innerHTML = data["prix_lettre_list"][i]["epaisseur_value"];
        cell5.innerHTML = data["prix_lettre_list"][i]["hauteur_value"] / 10;

        if (current_user_role === "admin") {
          cell6.innerHTML = `<input type="text" value='` + data["prix_lettre_list"][i]["prix"] + `'class='prix_text_input'>€`;
          cell7.innerHTML = `

                  <i type="button" class="delete_icon bi bi-trash text-danger " style="font-size: 20px;"
                  onclick="delete_Lettrebridge_row(this)"></i>
            `;
        } else {
          cell6.innerHTML = `<output type="text" >` + data["prix_lettre_list"][i]["prix"] + ` € </output>`;
        }
      }


    },
    error: function () {
      alert('Une erreur s\'est produite lors de fare l\'operation.');
    }
  });

});


function delete_Lettrebridge_row(current_bridge_row) {
  let text = "Attention!En supprimant cette client ,ca va supprimer automatiquement tous les commandes en cours de  ces informations.Voulez vous supprimer la cliente?";
  if (confirm(text)) {
    var row = current_bridge_row.parentNode.parentNode;
    var matiere = row.cells[1].innerHTML;
    var type = row.cells[2].innerHTML;
    var usinage = row.cells[3].innerHTML;
    var epaisseur = row.cells[4].innerHTML;


    let formData = new FormData();
    formData.append('matiere', matiere);
    formData.append('type', type);
    formData.append('usinage', usinage);
    formData.append('epaisseur', epaisseur);
    $.ajax({
      url: '/delete_Lettrebridge_row',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        console.log(msg);

        row.parentNode.removeChild(row);
        // Get the parent row of the button
        // row.parentNode.removeChild(row); // Remove the row from the table
        // var liste_clients_section = document.getElementById("edit_client_section");
        // liste_clients_section.style.display = "none";
        // window.location.href = "/clients";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }
}

$('#matieres_text_table').on('change', function (event) {
  var confirmed = confirm("Voulez-vous enregistrer les modifications ?");


  if (event.target.classList.contains('prix_text_input')) {
    if (confirmed) {
      const row = event.target.closest('tr');
      var newValue = row.querySelector('.prix_text_input').value;
      console.log(row);
      // var rec_user_id = row.querySelector('.rec_user_id').textContent;
      // var rec_client_id = row.querySelector('.rec_client_id').textContent;
      // Get data from the row
      var matiere = row.cells[1].innerHTML;
      var type = row.cells[2].innerHTML;
      var type_usinage = row.cells[3].innerHTML;
      var epaisseur = row.cells[4].innerHTML;
      var hauteur = row.cells[5].innerHTML * 10;

      let formData = new FormData();
      formData.append('new_prix', newValue);
      formData.append('matiere', matiere);
      formData.append('type_matiere', type);
      formData.append('type_usinage', type_usinage);
      formData.append('epaisseur', epaisseur);
      formData.append('hauteur', hauteur);

      $.ajax({
        url: '/edit_prix_lettre',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (msg) {

          console.log(msg)
          // var liste_clients_section = document.getElementById("edit_client_section");
          // liste_clients_section.style.display = "none";
          // window.location.href = "/clients";

        },
        error: function () {
          alert('Une erreur s\'est produite lors de fare l\'operation.');
        }
      });
    }
  }
});

function newUserForm() {
  var new_users_section = document.getElementById("new_users_section");
  new_users_section.style.display = "block";
}

function closeFormUser() {
  var new_users_section = document.getElementById("new_users_section");
  new_users_section.style.display = "none";
}




function addNewUser() {
  var selectRoleElement = document.getElementById("role_new_user");
  var selectRoleOption = selectRoleElement.options[selectRoleElement.selectedIndex];
  var selectedRoleValue = selectRoleOption.value;

  var name = document.getElementById("name_user");
  var nameText = name.value;


  var pwd = document.getElementById("pwd");
  var pwdText = pwd.value;


  var confirm_pwd = document.getElementById("confirm_pwd");
  var confirm_pwdText = confirm_pwd.value;

  var email = document.getElementById("email");
  var emailText = email.value;

  var tel = document.getElementById("telp");
  var telText = tel.value;
  if (confirm_pwdText != pwdText) {
    var errorMessage = document.getElementById('err_msg_div');
    errorMessage.style.display = 'block';
    document.getElementById("err_msg").innerHTML = "Le mot de passe doit être identique à sa confirmation!"
    setTimeout(() => {
      errorMessage.style.display = 'none';
    }, 1500);
  } else if (!nameText || !pwdText || !selectedRoleValue || !confirm_pwdText || !telText) {
    var errorMessage = document.getElementById('err_msg_div');
    errorMessage.style.display = 'block';
    document.getElementById("err_msg_membres").innerHTML = "Completez tout les cases demandées!"
    setTimeout(() => {
      errorMessage.style.display = 'none';
    }, 1500);
  } else {
    let formData = new FormData();
    formData.append('role', selectedRoleValue);
    formData.append('username', nameText);
    formData.append('email', emailText);
    formData.append('password', pwdText);
    formData.append('tel', telText);


    console.log(formData);

    $.ajax({
      url: '/new_user',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {

        console.log(msg)
        var new_users_section = document.getElementById("new_users_section");
        new_users_section.style.display = "none";
        window.location.href = "/membres";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }

}

function closeEditUser() {
  var edit_user_section = document.getElementById("edit_user_section");
  edit_user_section.style.display = "none";
}


$('#users_table').on('click', function (event) {


  // Check if the clicked element is a button with the class 'getInfoBtn'
  if (event.target.classList.contains('getInfoBtn')) {
    var edit_user_section = document.getElementById("edit_user_section");
    edit_user_section.style.display = "flex";
    // Find the parent row (tr) of the clicked button
    const row = event.target.closest('tr');
    var username = row.cells[1].innerHTML;
    var email = row.cells[2].innerHTML;
    var tel_span = row.querySelector('.user_pure_tel');
    var tel = tel_span.textContent.trim();

    var user_output = row.querySelector('.set_user_id');
    var user_output_id = user_output.textContent.trim();


    document.getElementById("name_edit_user").value = username;
    document.getElementById("edit_email").value = email;
    document.getElementById("edit_tel").value = tel;
    document.getElementById("edit_user_id").innerHTML = user_output_id;

    var selectRoleElement = document.getElementById("role_users");
    var selectRoleOption = selectRoleElement.options[selectRoleElement.selectedIndex];
    var selectedRoleValue = selectRoleOption.value;
    var selectedRoleText = selectRoleOption.innerText;

    var selectRole = document.getElementById("role_edit_user");
    // Loop through options to find the one with the desired value
    for (var i = 0; i < selectRole.options.length; i++) {
      if (selectRole.options[i].selected == true) {
        // Set the selected property to true for the found option
        selectRole.options[i].innerHTML = selectedRoleText;
        selectRole.options[i].value = selectedRoleValue;

        break;
      }
    }

    // var rec_user_id = row.querySelector('.rec_user_id').textContent;
    // var rec_client_id = row.querySelector('.rec_client_id').textContent;
    // // Get data from the row
    // var id = row.cells[0].value;
    // var name_rep = row.cells[1].innerText;
    // var name_client = row.cells[2].innerText;
    // var numero_voie_span = row.querySelector('.numero_voie_edit_span');
    // var name_voie_span = row.querySelector('.name_voie_edit_span');

    // // Get the value from the span element
    // var numero_voie_value = numero_voie_span.textContent.trim();
    // var name_voie_value = name_voie_span.textContent.trim();

    // var selectElement = document.getElementById("rep_edit_client");
    // // Loop through options to find the one with the desired value
    // for (var i = 0; i < selectElement.options.length; i++) {
    //   if (selectElement.options[i].selected == true) {
    //     // Set the selected property to true for the found option
    //     selectElement.options[i].innerHTML = name_rep;
    //     selectElement.options[i].value = rec_user_id;

    //     break;
    //   }
    // }
    // var cp = row.cells[4].innerText;



    // var ville = row.cells[5].innerText;
    // var email = row.cells[6].innerText;
    // var tel = row.cells[7].innerText;

    // document.getElementById("name_client_edit").value = name_client;
    // document.getElementById("numero_voie_edit").value = numero_voie_value;
    // document.getElementById("nom_voie_edit").value = name_voie_value;

    // document.getElementById("cp_edit").value = cp;
    // document.getElementById("ville_edit").value = ville;
    // document.getElementById("email_edit").value = email;
    // document.getElementById("telp_edit").value = tel;
    // document.getElementById("rec_client_id").innerHTML = rec_client_id;


  }
});


function openNewPasswordSpace() {
  close_pwd_change = document.getElementById("close_pwd_change");
  pwd_change = document.getElementById("pwd_change");
  close_pwd_change.style.display = "block";
  pwd_change.style.display = "none";
  new_pwd_div = document.getElementById("new_pwd_div");
  confirm_pwd_div = document.getElementById("confirm_pwd_div");
  new_pwd_div.style.display = "block";
  confirm_pwd_div.style.display = "block";
}


function closeNewPasswordSpace() {
  close_pwd_change = document.getElementById("close_pwd_change");
  pwd_change = document.getElementById("pwd_change");
  close_pwd_change.style.display = "none";
  pwd_change.style.display = "block";

  new_pwd_div = document.getElementById("new_pwd_div");
  confirm_pwd_div = document.getElementById("confirm_pwd_div");
  new_pwd_div.style.display = "none";
  confirm_pwd_div.style.display = "none";
}

function SaveEditUser() {
  alert("sd");
  var edit_user_id = document.getElementById("edit_user_id").innerHTML;

  var selectRoleElement = document.getElementById("role_edit_user");
  var selectRoleOption = selectRoleElement.options[selectRoleElement.selectedIndex];
  var selectedRoleValue = selectRoleOption.value;

  var name_edit_user = document.getElementById("name_edit_user").value;
  var edit_email = document.getElementById("edit_email").value;

  var new_pwd = document.getElementById("new_pwd").value;
  var new_confirm_pwd = document.getElementById("new_confirm_pwd").value;
  var edit_tel = document.getElementById("edit_tel").value;

  let formData = new FormData();
  formData.append('user_id', edit_user_id);
  formData.append('role', selectedRoleValue);
  formData.append('username', name_edit_user);
  formData.append('email', edit_email);
  formData.append('tel', edit_tel);
  console.log(formData);
  if (new_pwd_div.style.display == "block" && new_pwd !== new_confirm_pwd) {


    let errMsg = document.getElementById("errMsgMembers");
    errMsg.innerHTML = "Vérifier que les mdp sont identiques";
    console.log(errMsg);
    errMsg.classList.add('bg-danger');
    errMsg.style.display = "block";
    document.getElementById("new_pwd").style.border = '1px solid red';
    document.getElementById("new_confirm_pwd").style.border = '1px solid red';
    setTimeout(() => {
      errMsg.innerHTML = "";
      errMsg.style.display = 'none';
      document.getElementById("new_pwd").style.border = '0';
      document.getElementById("new_confirm_pwd").style.border = '0';
    }, 2500);
  } else if (new_pwd_div.style.display == "block" && (!new_pwd || !new_confirm_pwd)) {
    let errMsg = document.getElementById("errMsgMembers");
    errMsg.innerHTML = "Vérifier que les mdp sont pas vide";
    console.log(errMsg);
    errMsg.classList.add('bg-danger');
    errMsg.style.display = "block";
    document.getElementById("new_pwd").style.border = '1px solid red';
    document.getElementById("new_confirm_pwd").style.border = '1px solid red';
    setTimeout(() => {
      errMsg.innerHTML = "";
      errMsg.style.display = 'none';
      document.getElementById("new_pwd").style.border = '0';
      document.getElementById("new_confirm_pwd").style.border = '0';
    }, 2500);
  } else {
    if (new_pwd) {
      formData.append('new_pwd', new_pwd);
    }
    $.ajax({
      url: '/edit_user',
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function (msg) {
        window.location.href = "/membres";

      },
      error: function () {
        alert('Une erreur s\'est produite lors de fare l\'operation.');
      }
    });
  }
}





const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const validate = () => {

  clearErrorMsg();
  const $result_border = $('#email');
  const email = $('#email').val();
  if (email !== "") {
    $result_border.css('borderWidth', '3px')
    if (validateEmail(email)) {
      $result_border.css('borderColor', 'green');
    } else {

      $result_border.css('borderColor', '')
    }
  } else {
    $result_border.css('borderColor', '')
  }

}
function validatePassword() {
  clearErrorMsg();
  const $result_border = $('#password');
  const pwd = $('#password').val();
  if (pwd !== "" && pwd.length > 4) {
    $result_border.css('borderWidth', '3px')
    $result_border.css('borderColor', 'green');
  } else {
    $result_border.css('borderColor', '')
  }
}
$('#email').on('input', validate);
$('#password').on('input', validatePassword);

function clearErrorMsg() {
  var errorMessage = document.getElementById("errMsg");
  errorMessage.innerHTML = "";
}
function validateForm() {

  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;


  var errorMessageContainer = document.getElementById("errMsg");
  var isValid = true;
  errorMessageContainer.innerHTML = ""; // Clear previous error messages

  var emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  // Check if email is empty
  if (email.trim() == "" || password == "") {
    displayErrorMessage("Remplissez tous les champs");
    isValid = false;
  } else if (!emailRegex.test(email)) {
    displayErrorMessage("Adresse e-mail invalide");
    isValid = false;
  }


  return isValid;
}

function displayErrorMessage(message) {
  var errorMessage = document.getElementById("errMsg");
  errorMessage.innerHTML = message;
  document.getElementById("errMsg").style.display = "block"
  setTimeout(() => {
    errorMessage.style.display = 'none';
  }, 2000);
}


function closeAlert() {
  var alertElements = document.getElementsByClassName('alert');

  // Loop through each alert element and remove it
  for (var i = 0; i < alertElements.length; i++) {
    var alertElement = alertElements[i];
    alertElement.remove(); // Remove the element from the DOM
  }
}

function formValidatreCliennt(formData) {

  var representant = formData.get("representant");
  var name = formData.get('name');
  var numeroVoie = formData.get('numeroVoie');
  var nameVoie = formData.get('nameVoie');
  var cp = formData.get('cp');
  var ville = formData.get('ville');
  var email = formData.get('email');
  var prix_clent_livr = formData.get('prix_clent_livr');
  var tel = formData.get('tel');
  let msg = "";
  if (isAnyFormDataEmpty(formData)) {
    msg = "Un ou plusieurs champs du formulaire sont vides";
  } else {
    msg = "ggg"
  }

}
function isAnyFormDataEmpty(formData) {
  for (let [key, value] of formData.entries()) {
    if (typeof value === 'string' && value.trim() === "") {
      return true;
    }
  }
  return false;
}
function isNumber(value) {
  return !isNaN(Number(value));
}

// function validateForm() {
//   var name = document.getElementById("name").value;
//   var email = document.getElementById("email").value;
//   var password = document.getElementById("password").value;
//   var confirmPassword = document.getElementById("confirmPassword").value;
//   var errorMessageContainer = document.getElementById("errorMessages");
//   var isValid = true;
//   errorMessageContainer.innerHTML = ""; // Clear previous error messages

//   // Check if name is empty
//   if (name.trim() === "") {
//     displayErrorMessage("Name must be filled out");
//     isValid = false;
//   }

//   // Check if email is empty
//   if (email.trim() === "") {
//     displayErrorMessage("Email must be filled out");
//     isValid = false;
//   }

//   // Check if email is valid
//   var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   if (!emailRegex.test(email)) {
//     displayErrorMessage("Invalid email address");
//     isValid = false;
//   }

//   // Check if password is empty
//   if (password === "") {
//     displayErrorMessage("Password must be filled out");
//     isValid = false;
//   }

//   // Check if passwords match
//   if (password !== confirmPassword) {
//     displayErrorMessage("Passwords do not match");
//     isValid = false;
//   }

//   return isValid;
// }



window.setTimeout(function () {
  var alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {

    alert.classList.remove('show');
    alert.classList.add('fade');
    alert.style.display = "block";
    window.setTimeout(function () {
      alert.style.display = 'none';
    }, 150);  // Wait for the fade transition to complete (Bootstrap default transition time is 150ms)
  });
}, 2000);


function incrimentPlaqueSurface(button) {
  // Get the input element associated with this button
  const input = button.previousElementSibling;
  if (input && input.classList.contains('qte_plaque')) {
    // Get the current value of the input
    let currentValue = parseInt(input.value);
    if (!isNaN(currentValue)) {
      // Increment the value
      input.value = currentValue + 1;
      checkPlaquesValues();
      if (document.getElementById("add_new_plaque").style.display == "none") {
        input.value -= 1;
      }
    }
  }
}

function decrementPlaqueSurface(button) {
  // Get the input element associated with this button
  const input = button.nextElementSibling;
  if (input && input.classList.contains('qte_plaque')) {
    // Get the current value of the input
    let currentValue = parseInt(input.value);
    if (!isNaN(currentValue)) {
      if (currentValue > 1) {
        // Decrement the value
        input.value = currentValue - 1;
      } else if (currentValue == 1) {
        if (confirm("Voulez-vous supprimer cette sélection ?")) {
          const parentDiv = button.closest('.select_plaque_div');
          if (parentDiv) {
            parentDiv.remove();
          }
        }
      }
      checkPlaquesValues();

    }
  }
}



function change_input_plaque_surface(current) {
  let qte = current.value;

  if (qte < 0) {

    current.value = 1;
  }
};