import zipfile
import os

project_name = "recicla_app_sqlite"
dirs = [
    f"{project_name}/lib",
    f"{project_name}/assets",
    f"{project_name}/db",
]

files = {
    f"{project_name}/pubspec.yaml": """
name: recicla_app_sqlite
description: App Flutter com SQLite local para reciclagem
version: 1.0.0+1

environment:
  sdk: ">=2.17.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  sqflite: ^2.3.0
  path: ^1.8.3

flutter:
  uses-material-design: true
  assets:
    - assets/
    - db/
""",
    f"{project_name}/lib/main.dart": """
import 'package:flutter/material.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recicla App',
      home: ReciclaHomePage(),
    );
  }
}

class ReciclaHomePage extends StatefulWidget {
  @override
  _ReciclaHomePageState createState() => _ReciclaHomePageState();
}

class _ReciclaHomePageState extends State<ReciclaHomePage> {
  late Database db;
  TextEditingController controller = TextEditingController();
  String resultado = "";

  @override
  void initState() {
    super.initState();
    initDB();
  }

  Future<void> initDB() async {
    final dbPath = await getDatabasesPath();
    String path = join(dbPath, 'recicla.db');

    db = await openDatabase(path, version: 1, onCreate: (db, version) async {
      await db.execute('''
        CREATE TABLE produtos (
          id INTEGER PRIMARY KEY,
          nome TEXT,
          categoria TEXT,
          material TEXT,
          pode_reciclar INTEGER,
          dicas TEXT
        )
      ''');

      await db.insert('produtos', {
        'nome': 'Lata de Coca-Cola 350ml',
        'categoria': 'Metal',
        'material': 'Alumínio',
        'pode_reciclar': 1,
        'dicas': 'Lave bem; Amasse; Descarte em metal'
      });

      await db.insert('produtos', {
        'nome': 'Garrafa PET 500ml',
        'categoria': 'Plástico',
        'material': 'PET',
        'pode_reciclar': 1,
        'dicas': 'Lave; Retire rótulo; Descarte em plástico'
      });

      await db.insert('produtos', {
        'nome': 'Pilha AA',
        'categoria': 'Eletrônico',
        'material': 'Níquel',
        'pode_reciclar': 0,
        'dicas': 'Levar a ponto de coleta especial'
      });
    });
  }

  Future<void> buscarProduto(String nome) async {
    final List<Map<String, dynamic>> result = await db.query(
      'produtos',
      where: 'nome LIKE ?',
      whereArgs: ['%$nome%'],
    );

    if (result.isNotEmpty) {
      final produto = result.first;
      setState(() {
        resultado = '''
Produto: ${produto['nome']}
Categoria: ${produto['categoria']}
Material: ${produto['material']}
Pode Reciclar: ${produto['pode_reciclar'] == 1 ? "Sim" : "Não"}
Dicas: ${produto['dicas']}
''';
      });
    } else {
      setState(() {
        resultado = 'Produto não encontrado.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Recicla App")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: controller,
              decoration: InputDecoration(labelText: "Digite o nome do produto"),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () => buscarProduto(controller.text),
              child: Text("Buscar"),
            ),
            SizedBox(height: 20),
            Text(resultado),
          ],
        ),
      ),
    );
  }
""",
}

zip_filename = f"{project_name}.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    for filepath, content in files.items():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        zipf.write(filepath)
        os.remove(filepath)

print(f"Projeto salvo em: {zip_filename}")
