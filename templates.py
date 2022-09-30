def f_getTableTemplate():
    return """<table style='text-align: center;'>
<thead>
  <tr>
    <th></th>
    <th>Include Re-tweets</th>
    <th>Unique Tweets</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>#مهسا_امینی</td>
    <td>{:,d}</td>
    <td>{:,d}</td>
  </tr>
  <tr>
    <td>#MahsaAmini</td>
    <td>{:,d}</td>
    <td>{:,d}</td>
  </tr>
  <tr>
    <td>Any</td>
    <td>{:,d}</td>
    <td>{:,d}</td>
  </tr>
</tbody>
</table>"""
