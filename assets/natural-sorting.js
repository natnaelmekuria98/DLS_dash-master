/**
 * @author: Brian Huisman
 * @modder: Marco Aurélio Guerra
 * @webSite: http://www.greywyvern.com
 * JS functions to allow natural sorting on bootstrap-table columns
 * add data-sorter="alphanum" or data-sorter="numericOnly" to any th
 * 
 * Marco's Note: I had to modify the code to work with the dash bootstrap-table hack. 
 * i) in numericOnly added a regex search that accounts for negative number, original does not
 * ii) Added sortVariationWithTriangleOnly to deal with column that has triangle, it seems that in 
 *     this case the sort read the html object as string ( <p bla="bla" bla2="bla2"> string_I_want</p> )
 *     So I added a grep match to get the text from it.  
 */

function alphanum (a, b) {
  function chunkify (t) {
    const tz = []
    let y = -1
    let n = 0

    for (let i = 0; i <= t.length; i++) {
      const char = t.charAt(i)
      const charCode = char.charCodeAt(0)
      const m = (charCode === 46 || (charCode >= 48 && charCode <= 57))
      if (m !== n) {
        tz[++y] = ''
        n = m
      }
      tz[y] += char
    }

    return tz
  }

  function stringfy (v) {
    if (typeof(v) === 'number') {
      v = `${v}`
    }
    if (!v) {
      v = ''
    }
    return v
  }

  const aa = chunkify(stringfy(a))
  const bb = chunkify(stringfy(b))

  for (let x = 0; aa[x] && bb[x]; x++) {
    if (aa[x] !== bb[x]) {
      const c = Number(aa[x])
      const d = Number(bb[x])

      if (c === aa[x] && d === bb[x]) {
        return c - d
      }
      return (aa[x] > bb[x]) ? 1 : -1

    }
  }
  return aa.length - bb.length
}

// Sort variations with triangle and percentage
function sortVariationWithTriangleOnly(a, b) {


    
  function stripNonNumber (s) {
      if (s === "-" ) {
          return -999999999
      } else {

          // Read html string object and extract text from it  ... <p bla = "bal" bla2 = "bla2"> text_I_want </p>
          s = s.match("\>(.*)\<")[1]

          // Remove all non numeric and minus signal in the string to make it in to a integer
          s = s.replace(new RegExp(/[^\d.-]|\.(?=.*)/g), '')
          return parseInt(s, 10)
      }
  }

    return stripNonNumber(a) - stripNonNumber(b)
}

// Sort numerics disregarding letters ( Did not work for variation )
function numericOnly(a, b) {



    function stripNonNumber(s) {
        if (s === "-" | s === "nan") {
            return -999999999
        } else {

            // Remove all non numeric and minus signal in the string to make it in to a integer
            s = s.replace(new RegExp(/[^\d.-]|\.(?=.*)/g), '')
            return parseInt(s, 10)
        }
    }

    return stripNonNumber(a) - stripNonNumber(b)
}