import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    #-------------------------------------------------------------------------------------------------------------------------------------------
    def fillDDYear(self):

        anni = self._model.getAllYears()
        for a in anni:
            self._view.ddyear.options.append( ft.dropdown.Option(a) )

    def fillDDShape(self):

        shape = self._model.getAllShapes()
        for s in shape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))

    #------------------------------------------------------------------------------------------------------------------------------------------
    def handle_graph(self, e):

        anno = self._view.ddyear.value
        shape = self._view.ddshape.value

        if anno == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text( f"Attenzione, inserire un anno per continuare!", color="red"))
            self._view.update_page()
            return

        if shape == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text( f"Attenzione, inserire una shape per continuare!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(anno, shape)
        numNodi, numArchi = self._model.getDetailsGraph()
        listaPesiAdiacenti = self._model.getPesiAdiacenti()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {numNodi} \nNumero di archi: {numArchi}"))
        for t in listaPesiAdiacenti:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {t[0]}, somma pesi su archi = {t[1]}"))

        self._view.update_page()

    # ------------------------------------------------------------------------------------------------------------------------------------------


    def handle_path(self, e):
        pass