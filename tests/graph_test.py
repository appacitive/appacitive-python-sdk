__author__ = 'sathley'

from pyappacitive import AppacitiveGraphSearch
import nose, random


def get_random_string(number_of_characters=10):
    arr = [str(i) for i in range(number_of_characters)]
    random.shuffle(arr)
    return ''.join(arr)


def projection_test():
    val1 = get_random_string()
    val2 = get_random_string()







'''

string val1 = Unique.String, val2 = Unique.String;
            var root = await ObjectHelper.CreateNewAsync();
            var level1Child = ObjectHelper.NewInstance();
            level1Child.Set<string>("stringfield", val1);
            var level1Edge = Connection.New("link").FromExistingArticle("parent", root.Id).ToNewArticle("child", level1Child);
            await level1Edge.SaveAsync();

            var level2Child = ObjectHelper.NewInstance();
            level2Child.Set<string>("stringfield", val2);
            var level2Edge = Connection.New("link").FromExistingArticle("parent", level1Child.Id).ToNewArticle("child", level2Child);
            await level2Edge.SaveAsync();

            // Run filter
            var results = await Graph.Project("sample_project",
                new [] { root.Id },
                new Dictionary<string, string> { { "level1_filter", val1 }, { "level2_filter", val2 } });

            Assert.IsTrue(results.Count == 1);
            Assert.IsTrue(results[0].Article != null);
            Assert.IsTrue(results[0].Article.Id == root.Id);

            var level1Children = results[0].GetChildren("level1_children");
            Assert.IsTrue(level1Children.Count == 1);
            Assert.IsTrue(level1Children[0].Article != null);
            Assert.IsTrue(level1Children[0].Article.Id == level1Child.Id);
            Assert.IsTrue(level1Children[0].Connection != null);
            Assert.IsTrue(level1Children[0].Connection.Id == level1Edge.Id);
            Assert.IsTrue(level1Children[0].Connection.Endpoints["parent"].ArticleId == root.Id);
            Assert.IsTrue(level1Children[0].Connection.Endpoints["child"].ArticleId == level1Child.Id);

            var level2Children = level1Children[0].GetChildren("level2_children");
            Assert.IsTrue(level2Children.Count == 1);
            Assert.IsTrue(level2Children[0].Article != null);
            Assert.IsTrue(level2Children[0].Article.Id == level2Child.Id);
            Assert.IsTrue(level2Children[0].Connection != null);
            Assert.IsTrue(level2Children[0].Connection.Id == level2Edge.Id);
            Assert.IsTrue(level2Children[0].Connection.Endpoints["parent"].ArticleId == level1Child.Id);
            Assert.IsTrue(level2Children[0].Connection.Endpoints["child"].ArticleId == level2Child.Id);
'''