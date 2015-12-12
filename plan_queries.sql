SELECT SUM(doi.quantity), pr.name, pe.name, pe.quantity, pe.measure_unit, AVG(pc.buy_price), AVG(pc.sell_price)
FROM deliorders_orderitem doi
LEFT JOIN deliproducts_price pc ON doi.product_id = pc.id
LEFT JOIN deliproducts_presentation pe ON pc.presentation_id = pe.id
LEFT JOIN deliproducts_product pr ON pc.product_id = pr.id
GROUP BY pc.id

