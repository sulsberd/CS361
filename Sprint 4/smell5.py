 def __transmit_xml(self, req, data, oldsize):
        class G(xml.sax.saxutils.XMLGenerator):
            def doElement(self, name, value, attrs={}):
                self.startElement(name, attrs)
                if value is not None:
                    self.characters(value)
                self.endElement(name)

        s_io=StringIO.StringIO()
        g_object=G(s, 'utf-8')

        g_object.startDocument()
        g_object.startElement("res",
            {'max': str(self.last_id), 'saw': str(oldsize),
                'delivering': str(len(data)) })

        for datum in data:
            g_object.startElement("p", {})
            for sub_datum_1, sub_datum_2 in datum.iteritems():
                for info in sub_datum_2:
                    g_object.doElement(sub_datum_1, info)
            g_object.endElement("p")
        g_object.endElement("res")

        g_object.endDocument()

        s_io.seek(0, 0)
        req.write(self.__mk_res(req, s_io.read(), 'text/xml'))